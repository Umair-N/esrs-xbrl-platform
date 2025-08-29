import os
import json
import zipfile
import asyncio
import ijson
from io import BytesIO
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Generator, AsyncGenerator, Optional, List, Dict, Any, Union
from psycopg2.extras import RealDictCursor
from api.dep import get_current_user, get_db
from models.user import User
import logging
from functools import lru_cache
import time
from datetime import datetime, timedelta
import hashlib
import psycopg2
from contextlib import contextmanager

# Setup logging
logger = logging.getLogger(__name__)

# Initialize the router
router = APIRouter()

# Correct path to the zip file
ZIP_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../output/taxonomy_outline.zip'))

# Constants for optimization
CHUNK_SIZE = 64 * 1024  # 64KB chunks for better I/O performance
MAX_CONCURRENT_REQUESTS = 3  # Reduced for large file handling
DEFAULT_PAGE_SIZE = 1000  # Default items per response
MAX_PAGE_SIZE = 5000  # Maximum items per response
CACHE_TTL = 300  # 5 minutes cache TTL
MAX_SEARCH_DEPTH = 5  # Maximum depth for nested searches

# Semaphore to limit concurrency
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

# Simple in-memory cache for frequently accessed data
cache = {}
cache_timestamps = {}

class TaxonomyDatabaseManager:
    """Database manager for taxonomy data with PostgreSQL"""
    
    def __init__(self):
        self._create_tables_if_not_exists()
    
    def _create_tables_if_not_exists(self):
        """Create taxonomy tables if they don't exist"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS taxonomy_items (
            id SERIAL PRIMARY KEY,
            taxonomy_id VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(500) NOT NULL,
            description TEXT,
            parent_id INTEGER REFERENCES taxonomy_items(id) ON DELETE CASCADE,
            level INTEGER NOT NULL DEFAULT 0,
            path TEXT, -- Materialized path for efficient querying
            abstract BOOLEAN DEFAULT FALSE,
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- Indexes for performance
            INDEX idx_taxonomy_id (taxonomy_id),
            INDEX idx_parent_id (parent_id),
            INDEX idx_level (level),
            INDEX idx_path (path),
            INDEX idx_name (name),
            INDEX idx_abstract (abstract),
            INDEX idx_metadata (metadata) USING GIN
        );
        
        -- Full-text search index
        CREATE INDEX IF NOT EXISTS idx_taxonomy_fts 
        ON taxonomy_items USING GIN (to_tsvector('english', name || ' ' || COALESCE(description, '')));
        
        -- Function to update materialized path
        CREATE OR REPLACE FUNCTION update_taxonomy_path() 
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.parent_id IS NULL THEN
                NEW.path = NEW.id::TEXT;
                NEW.level = 0;
            ELSE
                SELECT path || '.' || NEW.id::TEXT, level + 1 
                INTO NEW.path, NEW.level
                FROM taxonomy_items 
                WHERE id = NEW.parent_id;
            END IF;
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Trigger to automatically update path and level
        DROP TRIGGER IF EXISTS trigger_update_taxonomy_path ON taxonomy_items;
        CREATE TRIGGER trigger_update_taxonomy_path
            BEFORE INSERT OR UPDATE ON taxonomy_items
            FOR EACH ROW EXECUTE FUNCTION update_taxonomy_path();
        
        -- Table for taxonomy import status
        CREATE TABLE IF NOT EXISTS taxonomy_imports (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'pending',
            total_items INTEGER DEFAULT 0,
            processed_items INTEGER DEFAULT 0,
            error_message TEXT,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            created_by INTEGER REFERENCES users(id)
        );
        """
        # Note: This would need to be executed during app startup with proper DB connection
    
    @contextmanager
    def get_cursor(self, db):
        """Get database cursor with proper error handling"""
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            db.commit()
        except Exception as error:
            db.rollback()
            raise error
        finally:
            cursor.close()
    
    async def get_paginated_taxonomy(
        self, 
        db,
        page: int = 1, 
        page_size: int = DEFAULT_PAGE_SIZE,
        parent_id: Optional[int] = None,
        level: Optional[int] = None,
        search_query: Optional[str] = None,
        abstract_only: Optional[bool] = None,
        include_children: bool = True,
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get paginated taxonomy data from database"""
        
        offset = (page - 1) * page_size
        
        # Build base query
        base_conditions = []
        query_params = {"limit": page_size, "offset": offset}
        
        if parent_id is not None:
            if parent_id == 0:
                base_conditions.append("parent_id IS NULL")
            else:
                base_conditions.append("parent_id = %(parent_id)s")
                query_params["parent_id"] = parent_id
        
        if level is not None:
            base_conditions.append("level = %(level)s")
            query_params["level"] = level
        
        if abstract_only is not None:
            base_conditions.append("abstract = %(abstract)s")
            query_params["abstract"] = abstract_only
        
        if search_query:
            base_conditions.append(
                "to_tsvector('english', name || ' ' || COALESCE(description, '')) @@ plainto_tsquery('english', %(search_query)s)"
            )
            query_params["search_query"] = search_query
        
        where_clause = " AND ".join(base_conditions) if base_conditions else "TRUE"
        
        # Main query
        main_query = f"""
        SELECT 
            id, taxonomy_id, name, description, parent_id, level, path, abstract, metadata,
            created_at, updated_at
        FROM taxonomy_items 
        WHERE {where_clause}
        ORDER BY level ASC, name ASC
        LIMIT %(limit)s OFFSET %(offset)s
        """
        
        # Count query
        count_query = f"""
        SELECT COUNT(*) as total
        FROM taxonomy_items 
        WHERE {where_clause}
        """
        
        with self.get_cursor(db) as cursor:
            # Get items
            cursor.execute(main_query, query_params)
            items = cursor.fetchall()
            
            # Get total count
            cursor.execute(count_query, {k: v for k, v in query_params.items() if k not in ['limit', 'offset']})
            total_count = cursor.fetchone()['total']
            
            # Add children if requested
            if include_children and items:
                items_with_children = []
                for item in items:
                    item_dict = dict(item)
                    
                    if include_children:
                        children = await self._get_children(
                            db, item['id'], max_depth - 1 if max_depth else None
                        )
                        item_dict['children'] = children
                        item_dict['children_count'] = len(children)
                    
                    items_with_children.append(item_dict)
                
                items = items_with_children
            else:
                items = [dict(item) for item in items]
        
        return {
            "success": True,
            "data": items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total_count,
                "total_pages": (total_count + page_size - 1) // page_size,
                "has_next": page * page_size < total_count,
                "has_prev": page > 1
            },
            "metadata": {
                "timestamp": time.time(),
                "source": "database"
            }
        }
    
    async def _get_children(self, db, parent_id: int, max_depth: Optional[int] = None) -> List[Dict]:
        """Recursively get children for a taxonomy item"""
        if max_depth == 0:
            return []
        
        query = """
        SELECT id, taxonomy_id, name, description, parent_id, level, path, abstract, metadata,
               created_at, updated_at
        FROM taxonomy_items 
        WHERE parent_id = %s
        ORDER BY name ASC
        """
        
        with self.get_cursor(db) as cursor:
            cursor.execute(query, (parent_id,))
            children = cursor.fetchall()
            
            children_list = []
            for child in children:
                child_dict = dict(child)
                
                # Recursively get grandchildren if depth allows
                if max_depth is None or max_depth > 1:
                    next_depth = max_depth - 1 if max_depth else None
                    grandchildren = await self._get_children(db, child['id'], next_depth)
                    child_dict['children'] = grandchildren
                    child_dict['children_count'] = len(grandchildren)
                else:
                    child_dict['children'] = []
                    child_dict['children_count'] = 0
                
                children_list.append(child_dict)
            
            return children_list
    
    async def get_taxonomy_stats(self, db) -> Dict[str, Any]:
        """Get comprehensive taxonomy statistics"""
        stats_query = """
        SELECT 
            COUNT(*) as total_items,
            COUNT(CASE WHEN parent_id IS NULL THEN 1 END) as root_items,
            COUNT(CASE WHEN abstract = true THEN 1 END) as abstract_items,
            COUNT(CASE WHEN abstract = false THEN 1 END) as concrete_items,
            MAX(level) as max_depth,
            AVG(level) as avg_depth
        FROM taxonomy_items;
        
        SELECT level, COUNT(*) as count
        FROM taxonomy_items 
        GROUP BY level 
        ORDER BY level;
        """
        
        with self.get_cursor(db) as cursor:
            # Get overall stats
            cursor.execute("""
            SELECT 
                COUNT(*) as total_items,
                COUNT(CASE WHEN parent_id IS NULL THEN 1 END) as root_items,
                COUNT(CASE WHEN abstract = true THEN 1 END) as abstract_items,
                COUNT(CASE WHEN abstract = false THEN 1 END) as concrete_items,
                MAX(level) as max_depth,
                AVG(level) as avg_depth
            FROM taxonomy_items
            """)
            overall_stats = cursor.fetchone()
            
            # Get level distribution
            cursor.execute("""
            SELECT level, COUNT(*) as count
            FROM taxonomy_items 
            GROUP BY level 
            ORDER BY level
            """)
            level_distribution = {row['level']: row['count'] for row in cursor.fetchall()}
        
        return {
            "total_items": overall_stats['total_items'],
            "root_items": overall_stats['root_items'],
            "abstract_items": overall_stats['abstract_items'],
            "concrete_items": overall_stats['concrete_items'],
            "max_depth": overall_stats['max_depth'],
            "average_depth": float(overall_stats['avg_depth']) if overall_stats['avg_depth'] else 0,
            "level_distribution": level_distribution,
            "timestamp": time.time()
        }
    
    async def search_taxonomy(
        self, 
        db,
        query: str,
        field: str = "name",
        limit: int = 100,
        include_children: bool = False
    ) -> List[Dict]:
        """Full-text search in taxonomy"""
        
        if field == "name":
            search_query = """
            SELECT id, taxonomy_id, name, description, parent_id, level, path, abstract, metadata,
                   ts_rank_cd(to_tsvector('english', name), plainto_tsquery('english', %s)) as rank
            FROM taxonomy_items 
            WHERE to_tsvector('english', name) @@ plainto_tsquery('english', %s)
            ORDER BY rank DESC, name ASC
            LIMIT %s
            """
        else:
            search_query = """
            SELECT id, taxonomy_id, name, description, parent_id, level, path, abstract, metadata,
                   ts_rank_cd(to_tsvector('english', name || ' ' || COALESCE(description, '')), plainto_tsquery('english', %s)) as rank
            FROM taxonomy_items 
            WHERE to_tsvector('english', name || ' ' || COALESCE(description, '')) @@ plainto_tsquery('english', %s)
            ORDER BY rank DESC, name ASC
            LIMIT %s
            """
        
        with self.get_cursor(db) as cursor:
            cursor.execute(search_query, (query, query, limit))
            results = cursor.fetchall()
            
            search_results = []
            for result in results:
                result_dict = dict(result)
                result_dict.pop('rank', None)  # Remove rank from final result
                
                if include_children:
                    children = await self._get_children(db, result['id'], 2)  # Limit to 2 levels for search
                    result_dict['children'] = children
                    result_dict['children_count'] = len(children)
                
                search_results.append(result_dict)
            
            return search_results
    
    async def import_from_json(self, db, user_id: int, background_tasks: BackgroundTasks):
        """Import taxonomy data from JSON file to database"""
        
        # Create import record
        with self.get_cursor(db) as cursor:
            cursor.execute("""
                INSERT INTO taxonomy_imports (filename, status, created_by)
                VALUES (%s, %s, %s) RETURNING id
            """, ("taxonomy_outline.json", "processing", user_id))
            import_id = cursor.fetchone()['id']
        
        # Schedule background task
        background_tasks.add_task(self._process_import, db, import_id)
        
        return {"import_id": import_id, "status": "started"}
    
    async def _process_import(self, db, import_id: int):
        """Background task to process taxonomy import"""
        try:
            # Read from zip file
            with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
                file_content = zip_ref.read("taxonomy_outline.json")
                file_buffer = BytesIO(file_content)
            
            parser = ijson.items(file_buffer, 'item')
            
            processed_items = 0
            batch_size = 100
            batch_items = []
            
            with self.get_cursor(db) as cursor:
                # Clear existing data
                cursor.execute("DELETE FROM taxonomy_items")
                
                for item in parser:
                    batch_items.append(item)
                    
                    if len(batch_items) >= batch_size:
                        await self._insert_batch(cursor, batch_items, None)
                        processed_items += len(batch_items)
                        
                        # Update progress
                        cursor.execute("""
                            UPDATE taxonomy_imports 
                            SET processed_items = %s 
                            WHERE id = %s
                        """, (processed_items, import_id))
                        
                        batch_items = []
                
                # Process remaining items
                if batch_items:
                    await self._insert_batch(cursor, batch_items, None)
                    processed_items += len(batch_items)
                
                # Mark as completed
                cursor.execute("""
                    UPDATE taxonomy_imports 
                    SET status = %s, processed_items = %s, total_items = %s, completed_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, ("completed", processed_items, processed_items, import_id))
            
            logger.info(f"Import {import_id} completed successfully. Processed {processed_items} items.")
            
        except Exception as e:
            logger.error(f"Import {import_id} failed: {str(e)}")
            
            with self.get_cursor(db) as cursor:
                cursor.execute("""
                    UPDATE taxonomy_imports 
                    SET status = %s, error_message = %s, completed_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, ("failed", str(e), import_id))
    
    async def _insert_batch(self, cursor, items: List[Dict], parent_db_id: Optional[int]):
        """Insert a batch of taxonomy items"""
        for item in items:
            # Insert main item
            cursor.execute("""
                INSERT INTO taxonomy_items (taxonomy_id, name, description, parent_id, abstract, metadata)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, (
                item.get('id', ''),
                item.get('name', ''),
                item.get('description', ''),
                parent_db_id,
                item.get('abstract') == 'true',
                json.dumps(item.get('metadata', {}))
            ))
            
            item_db_id = cursor.fetchone()['id']
            
            # Insert children recursively
            if 'children' in item and item['children']:
                await self._insert_batch(cursor, item['children'], item_db_id)

class TaxonomyDataManager:
    """Hybrid taxonomy data manager supporting both file and database operations"""

    def __init__(self, zip_path: str):
        self.zip_path = zip_path
        self.db_manager = TaxonomyDatabaseManager()
        self._validate_zip_file()

    def _validate_zip_file(self):
        """Validate zip file exists and is accessible"""
        if not os.path.exists(self.zip_path):
            raise HTTPException(status_code=404, detail="Taxonomy zip file not found")

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.testzip()
        except zipfile.BadZipFile:
            raise HTTPException(status_code=500, detail="Corrupted zip file")

    def _get_cache_key(self, **kwargs) -> str:
        """Generate cache key from parameters"""
        cache_data = json.dumps(kwargs, sort_keys=True)
        return hashlib.md5(cache_data.encode()).hexdigest()

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid"""
        if cache_key not in cache_timestamps:
            return False
        return (time.time() - cache_timestamps[cache_key]) < CACHE_TTL

    def _set_cache(self, cache_key: str, data: Any):
        """Set cache entry"""
        cache[cache_key] = data
        cache_timestamps[cache_key] = time.time()

    def _get_cache(self, cache_key: str) -> Optional[Any]:
        """Get cache entry if valid"""
        if self._is_cache_valid(cache_key):
            return cache.get(cache_key)
        return None

    async def get_paginated_data(
        self, 
        db = None,
        file_name: Optional[str] = None,
        use_database: bool = True,
        page: int = 1, 
        page_size: int = DEFAULT_PAGE_SIZE,
        parent_id: Optional[int] = None,
        level: Optional[int] = None,
        filter_key: Optional[str] = None,
        filter_value: Optional[str] = None,
        search_query: Optional[str] = None,
        search_field: Optional[str] = None,
        abstract_only: Optional[bool] = None,
        include_children: bool = True,
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get paginated taxonomy data from database or file
        """
        # Try database first if available
        if use_database and db:
            try:
                return await self.db_manager.get_paginated_taxonomy(
                    db=db,
                    page=page,
                    page_size=page_size,
                    parent_id=parent_id,
                    level=level,
                    search_query=search_query,
                    abstract_only=abstract_only,
                    include_children=include_children,
                    max_depth=max_depth
                )
            except Exception as e:
                logger.warning(f"Database query failed, falling back to file: {str(e)}")
        
        # Fallback to file-based approach (your existing implementation)
        # Generate cache key
        cache_key = self._get_cache_key(
            file_name=file_name, page=page, page_size=page_size,
            filter_key=filter_key, filter_value=filter_value,
            search_query=search_query, search_field=search_field,
            include_children=include_children, max_depth=max_depth
        )

        # Check cache first
        cached_result = self._get_cache(cache_key)
        if cached_result:
            logger.info(f"Returning cached result for page {page}")
            return cached_result

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                if file_name not in zip_ref.namelist():
                    raise HTTPException(status_code=404, detail="File not found in zip archive")

                file_content = zip_ref.read(file_name)
                file_buffer = BytesIO(file_content)

            # Calculate pagination
            offset = (page - 1) * page_size
            items_collected = []
            items_skipped = 0
            total_processed = 0

            # Stream parse the JSON array
            parser = ijson.items(file_buffer, 'item')

            for item in parser:
                total_processed += 1

                # Apply filtering if specified
                if filter_key and filter_value:
                    if not self._matches_filter(item, filter_key, filter_value):
                        continue

                # Apply search if specified
                if search_query and search_field:
                    if not self._matches_search(item, search_query, search_field, max_depth):
                        continue

                # Handle pagination offset
                if items_skipped < offset:
                    items_skipped += 1
                    continue

                # Collect items for current page
                if len(items_collected) < page_size:
                    # Process hierarchical data if needed
                    processed_item = self._process_hierarchical_item(
                        item, include_children, max_depth
                    )
                    items_collected.append(processed_item)
                else:
                    # We have enough items, stop processing
                    break

                # Yield control periodically for large datasets
                if total_processed % 1000 == 0:
                    await asyncio.sleep(0)

            # Calculate metadata
            has_more = len(items_collected) == page_size
            total_items_estimate = None

            # For first page without filters, try to estimate total
            if page == 1 and not filter_key and not search_query:
                if items_collected:
                    avg_item_size = len(json.dumps(items_collected[0]))
                    total_items_estimate = len(file_content) // avg_item_size

            response_data = {
                "success": True,
                "data": items_collected,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "items_count": len(items_collected),
                    "has_more": has_more,
                    "total_processed": total_processed
                },
                "metadata": {
                    "file_name": file_name,
                    "timestamp": time.time(),
                    "estimated_total": total_items_estimate,
                    "cached": False,
                    "source": "file"
                }
            }

            # Add filter info if applied
            if filter_key and filter_value:
                response_data["filter"] = {
                    "key": filter_key,
                    "value": filter_value
                }

            # Add search info if applied
            if search_query and search_field:
                response_data["search"] = {
                    "query": search_query,
                    "field": search_field,
                    "max_depth": max_depth
                }

            # Cache the result for future requests
            self._set_cache(cache_key, response_data)

            logger.info(f"Returned {len(items_collected)} items from {file_name} (page {page})")
            return response_data

        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Invalid JSON format: {str(e)}")
        except MemoryError:
            raise HTTPException(status_code=500, detail="File too large to process")
        except Exception as e:
            logger.error(f"Error processing taxonomy data: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    def _process_hierarchical_item(
        self, 
        item: dict, 
        include_children: bool = True, 
        max_depth: Optional[int] = None
    ) -> dict:
        """Process hierarchical taxonomy item with depth control"""
        if not include_children or max_depth == 0:
            # Remove children if not requested or max depth reached
            item_copy = item.copy()
            if 'children' in item_copy:
                item_copy['children'] = []
                item_copy['children_count'] = len(item.get('children', []))
            return item_copy

        # Recursively process children with depth limit
        if 'children' in item and item['children']:
            processed_children = []
            next_depth = max_depth - 1 if max_depth else None

            for child in item['children']:
                processed_child = self._process_hierarchical_item(
                    child, include_children, next_depth
                )
                processed_children.append(processed_child)

            item_copy = item.copy()
            item_copy['children'] = processed_children
            return item_copy

        return item

    async def stream_data_as_response(
        self,
        file_name: str,
        limit: Optional[int] = None,
        filter_key: Optional[str] = None,
        filter_value: Optional[str] = None,
        include_children: bool = False,
        format_type: str = "ndjson"
    ) -> AsyncGenerator[str, None]:
        """
        Stream data as Server-Sent Events, NDJSON, or JSON Array for real-time consumption
        """
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                if file_name not in zip_ref.namelist():
                    raise HTTPException(status_code=404, detail="File not found in zip archive")

                file_content = zip_ref.read(file_name)
                file_buffer = BytesIO(file_content)

            items_streamed = 0
            parser = ijson.items(file_buffer, 'item')

            # Different formats need different handling
            if format_type == "json":
                # Start JSON array
                yield "{\n"
                yield '  "metadata": {\n'
                yield f'    "timestamp": {time.time()},\n'
                yield f'    "file_name": "{file_name}"\n'
                yield '  },\n'
                yield '  "data": [\n'

                first_item = True

                for item in parser:
                    # Apply limit
                    if limit and items_streamed >= limit:
                        break

                    # Apply filtering
                    if filter_key and filter_value:
                        if not self._matches_filter(item, filter_key, filter_value):
                            continue

                    # Process hierarchical data
                    processed_item = self._process_hierarchical_item(
                        item, include_children, max_depth=2
                    )

                    # Add comma for all items except the first
                    if not first_item:
                        yield ",\n"
                    else:
                        first_item = False

                    # Yield data item
                    yield f'    {json.dumps(processed_item, indent=4).replace(chr(10), chr(10) + "    ")}'

                    items_streamed += 1

                    # Yield control periodically
                    if items_streamed % 100 == 0:
                        await asyncio.sleep(0)

                # Close JSON array and object
                yield '\n  ],\n'
                yield '  "summary": {\n'
                yield f'    "total_streamed": {items_streamed},\n'
                yield '    "completed": true\n'
                yield '  }\n'
                yield "}\n"

            elif format_type == "sse":
                # Server-Sent Events format
                yield f"data: {json.dumps({'type': 'metadata', 'timestamp': time.time(), 'file_name': file_name})}\n\n"

                for item in parser:
                    if limit and items_streamed >= limit:
                        break

                    if filter_key and filter_value:
                        if not self._matches_filter(item, filter_key, filter_value):
                            continue

                    processed_item = self._process_hierarchical_item(
                        item, include_children, max_depth=2
                    )

                    yield f"data: {json.dumps({'type': 'data', 'item': processed_item, 'index': items_streamed})}\n\n"

                    items_streamed += 1

                    if items_streamed % 100 == 0:
                        await asyncio.sleep(0)

                yield f"data: {json.dumps({'type': 'summary', 'total_streamed': items_streamed, 'completed': True})}\n\n"

            else:  # ndjson format
                # Start with metadata
                yield json.dumps({
                    "type": "metadata",
                    "timestamp": time.time(),
                    "file_name": file_name
                }) + "\n"

                for item in parser:
                    if limit and items_streamed >= limit:
                        break

                    if filter_key and filter_value:
                        if not self._matches_filter(item, filter_key, filter_value):
                            continue

                    processed_item = self._process_hierarchical_item(
                        item, include_children, max_depth=2
                    )

                    yield json.dumps({
                        "type": "data",
                        "item": processed_item,
                        "index": items_streamed
                    }) + "\n"

                    items_streamed += 1

                    if items_streamed % 100 == 0:
                        await asyncio.sleep(0)

                # End with summary
                yield json.dumps({
                    "type": "summary",
                    "total_streamed": items_streamed,
                    "completed": True
                }) + "\n"

        except Exception as e:
            error_obj = {"type": "error", "error": str(e)}
            if format_type == "json":
                yield f'{{"error": "{str(e)}"}}\n'
            elif format_type == "sse":
                yield f"data: {json.dumps(error_obj)}\n\n"
            else:
                yield json.dumps(error_obj) + "\n"

    def _matches_filter(self, item: dict, filter_key: str, filter_value: str) -> bool:
        """Check if item matches filter criteria with hierarchical support"""
        try:
            # Check main item
            if self._check_nested_value(item, filter_key, filter_value):
                return True

            # Check children if they exist
            if 'children' in item and item['children']:
                for child in item['children']:
                    if self._matches_filter(child, filter_key, filter_value):
                        return True

            return False
        except (AttributeError, KeyError):
            return False

    def _matches_search(
        self, 
        item: dict, 
        search_query: str, 
        search_field: str, 
        max_depth: Optional[int] = None
    ) -> bool:
        """Check if item matches search criteria with hierarchical support"""
        try:
            # Check main item
            if self._check_nested_search(item, search_query, search_field):
                return True

            # Check children if they exist and depth allows
            if max_depth is None or max_depth > 0:
                if 'children' in item and item['children']:
                    next_depth = max_depth - 1 if max_depth else None
                    for child in item['children']:
                        if self._matches_search(child, search_query, search_field, next_depth):
                            return True

            return False
        except (AttributeError, KeyError):
            return False

    def _check_nested_value(self, item: dict, key_path: str, target_value: str) -> bool:
        """Check nested value using dot notation"""
        keys = key_path.split('.')
        value = item
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return False
        return str(value).lower() == target_value.lower()

    def _check_nested_search(self, item: dict, search_query: str, key_path: str) -> bool:
        """Check nested search using dot notation"""
        keys = key_path.split('.')
        value = item
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return False
        return search_query.lower() in str(value).lower()

    async def get_file_metadata(self, file_name: str) -> Dict[str, Any]:
        """Get detailed metadata about the JSON file"""
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                if file_name not in zip_ref.namelist():
                    raise HTTPException(status_code=404, detail="File not found")

                file_info = zip_ref.getinfo(file_name)
                file_content = zip_ref.read(file_name)

                # Sample first few items for structure analysis
                file_buffer = BytesIO(file_content)
                parser = ijson.items(file_buffer, 'item')
                sample_items = []

                for i, item in enumerate(parser):
                    if i >= 3:  # Get first 3 items
                        break
                    sample_items.append(item)

                # Analyze structure
                fields = set()
                max_depth = 0
                total_children = 0

                if sample_items:
                    for item in sample_items:
                        if isinstance(item, dict):
                            fields.update(item.keys())
                            depth, children_count = self._analyze_depth(item)
                            max_depth = max(max_depth, depth)
                            total_children += children_count

                return {
                    "filename": file_name,
                    "compressed_size": file_info.compress_size,
                    "uncompressed_size": file_info.file_size,
                    "last_modified": file_info.date_time,
                    "sample_structure": {
                        "fields": list(fields),
                        "sample_count": len(sample_items),
                        "max_depth": max_depth,
                        "total_children_in_sample": total_children,
                        "first_item": sample_items[0] if sample_items else None
                    }
                }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting file metadata: {str(e)}")

    def _analyze_depth(self, item: dict, current_depth: int = 1) -> tuple[int, int]:
        """Analyze maximum depth and count children in hierarchical structure"""
        max_depth = current_depth
        children_count = 0

        if 'children' in item and item['children']:
            children_count = len(item['children'])
            for child in item['children']:
                child_depth, child_children = self._analyze_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
                children_count += child_children

        return max_depth, children_count

# Initialize data manager
taxonomy_manager = TaxonomyDataManager(ZIP_FILE_PATH)

# Main endpoint - returns complete JSON response with pagination
@router.get("", response_model=dict)
async def get_taxonomy_data(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Items per page"),
    parent_id: Optional[int] = Query(None, description="Parent ID to filter children (0 for root items)"),
    level: Optional[int] = Query(None, ge=0, description="Hierarchy level to filter"),
    filter_key: Optional[str] = Query(None, description="Key to filter on (supports dot notation)"),
    filter_value: Optional[str] = Query(None, description="Value to match for filtering"),
    search_query: Optional[str] = Query(None, description="Search term"),
    search_field: Optional[str] = Query("name", description="Field to search in"),
    abstract_only: Optional[bool] = Query(None, description="Filter by abstract items only"),
    include_children: bool = Query(True, description="Include children in response"),
    max_depth: Optional[int] = Query(None, ge=1, le=10, description="Maximum depth to include"),
    use_database: bool = Query(True, description="Use database if available, fallback to file"),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
) -> JSONResponse:
    """
    Get taxonomy data as paginated JSON response with hierarchical support
    Supports both database and file-based queries with automatic fallback
    """
    async with semaphore:
        file_name = "taxonomy_outline.json"

        try:
            result = await taxonomy_manager.get_paginated_data(
                db=db if use_database else None,
                file_name=file_name,
                use_database=use_database,
                page=page,
                page_size=page_size,
                parent_id=parent_id,
                level=level,
                filter_key=filter_key,
                filter_value=filter_value,
                search_query=search_query,
                search_field=search_field,
                abstract_only=abstract_only,
                include_children=include_children,
                max_depth=max_depth
            )

            return JSONResponse(content=result, status_code=200)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_taxonomy_data: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

# Streaming endpoint for real-time data consumption
@router.get("/stream", response_class=StreamingResponse)
async def stream_taxonomy_data(
    limit: Optional[int] = Query(None, ge=1, le=50000, description="Maximum items to stream"),
    filter_key: Optional[str] = Query(None, description="Key to filter on"),
    filter_value: Optional[str] = Query(None, description="Value to match"),
    include_children: bool = Query(False, description="Include children in stream"),
    format_type: str = Query("ndjson", regex="^(ndjson|sse|json)$", description="Stream format (ndjson, sse, or json)"),
    current_user: User = Depends(get_current_user)
):
    """
    Stream taxonomy data as NDJSON, Server-Sent Events, or JSON Array

    - **ndjson**: Each line is a separate JSON object (for streaming processors)
    - **sse**: Server-Sent Events format (for web browsers)  
    - **json**: Regular JSON array (parseable by standard JSON parsers)
    """
    async with semaphore:
        file_name = "taxonomy_outline.json"

        if format_type == "json":
            media_type = "application/json"
        elif format_type == "ndjson":
            media_type = "application/x-ndjson"
        else:
            media_type = "text/event-stream"

        return StreamingResponse(
            taxonomy_manager.stream_data_as_response(
                file_name, limit, filter_key, filter_value, include_children, format_type
            ),
            media_type=media_type,
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # Disable nginx buffering
            }
        )

# Database-specific endpoints
@router.post("/import", response_model=dict)
async def import_taxonomy_to_database(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
) -> JSONResponse:
    """
    Import taxonomy data from JSON file to PostgreSQL database
    This is a background operation that processes the entire taxonomy
    """
    try:
        result = await taxonomy_manager.db_manager.import_from_json(
            db=db, 
            user_id=current_user.id, 
            background_tasks=background_tasks
        )
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Import started successfully",
                "import_id": result["import_id"]
            },
            status_code=202
        )
    except Exception as e:
        logger.error(f"Error starting import: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start import process")

@router.get("/import/status/{import_id}", response_model=dict)
async def get_import_status(
    import_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
) -> JSONResponse:
    """Get the status of a taxonomy import operation"""
    try:
        with taxonomy_manager.db_manager.get_cursor(db) as cursor:
            cursor.execute("""
                SELECT status, total_items, processed_items, error_message, 
                       started_at, completed_at
                FROM taxonomy_imports 
                WHERE id = %s AND created_by = %s
            """, (import_id, current_user.id))
            
            import_status = cursor.fetchone()
            
            if not import_status:
                raise HTTPException(status_code=404, detail="Import not found")
            
            result = {
                "import_id": import_id,
                "status": import_status['status'],
                "total_items": import_status['total_items'],
                "processed_items": import_status['processed_items'],
                "started_at": import_status['started_at'].isoformat() if import_status['started_at'] else None,
                "completed_at": import_status['completed_at'].isoformat() if import_status['completed_at'] else None
            }
            
            if import_status['error_message']:
                result['error_message'] = import_status['error_message']
            
            if import_status['total_items'] and import_status['total_items'] > 0:
                result['progress_percentage'] = (
                    import_status['processed_items'] / import_status['total_items'] * 100
                )
            
            return JSONResponse(content=result, status_code=200)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting import status: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving import status")

# Metadata endpoint
@router.get("/info", response_model=dict)
async def get_taxonomy_info(
    use_database: bool = Query(True, description="Get info from database if available"),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
) -> JSONResponse:
    """Get detailed metadata about the taxonomy"""
    try:
        if use_database:
            try:
                # Try database first
                stats = await taxonomy_manager.db_manager.get_taxonomy_stats(db)
                
                # Add database-specific info
                with taxonomy_manager.db_manager.get_cursor(db) as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) as import_count,
                               MAX(completed_at) as last_import
                        FROM taxonomy_imports 
                        WHERE status = 'completed'
                    """)
                    import_info = cursor.fetchone()
                
                result = {
                    "source": "database",
                    "statistics": stats,
                    "import_info": {
                        "total_imports": import_info['import_count'],
                        "last_import": import_info['last_import'].isoformat() if import_info['last_import'] else None
                    },
                    "timestamp": time.time()
                }
                
                return JSONResponse(content=result, status_code=200)
                
            except Exception as db_error:
                logger.warning(f"Database info failed, falling back to file: {str(db_error)}")
        
        # Fallback to file-based info
        file_name = "taxonomy_outline.json"
        metadata = await taxonomy_manager.get_file_metadata(file_name)
        metadata["source"] = "file"
        
        return JSONResponse(content=metadata, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting taxonomy info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving taxonomy information")

# Hierarchy statistics endpoint
@router.get("/stats", response_model=dict)
async def get_taxonomy_stats(
    use_database: bool = Query(True, description="Get stats from database if available"),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
) -> JSONResponse:
    """Get hierarchy statistics for the taxonomy"""
    try:
        if use_database:
            try:
                stats = await taxonomy_manager.db_manager.get_taxonomy_stats(db)
                stats["source"] = "database"
                return JSONResponse(content=stats, status_code=200)
            except Exception as db_error:
                logger.warning(f"Database stats failed, falling back to file: {str(db_error)}")
        
        # Fallback to file-based stats (you'd need to implement this method)
        file_name = "taxonomy_outline.json"
        
        # Simple file-based stats
        try:
            with zipfile.ZipFile(taxonomy_manager.zip_path, 'r') as zip_ref:
                file_content = zip_ref.read(file_name)
                file_buffer = BytesIO(file_content)

            parser = ijson.items(file_buffer, 'item')
            
            total_items = 0
            max_depth = 0
            abstract_count = 0
            
            for item in parser:
                total_items += 1
                
                # Simple depth calculation
                item_depth, _ = taxonomy_manager._analyze_depth(item)
                max_depth = max(max_depth, item_depth)
                
                if item.get('abstract') == 'true':
                    abstract_count += 1
                
                # Yield control periodically
                if total_items % 1000 == 0:
                    await asyncio.sleep(0)
            
            stats = {
                "source": "file",
                "total_items": total_items,
                "max_depth": max_depth,
                "abstract_items": abstract_count,
                "concrete_items": total_items - abstract_count,
                "timestamp": time.time()
            }
            
            return JSONResponse(content=stats, status_code=200)
            
        except Exception as file_error:
            raise HTTPException(status_code=500, detail=f"Error processing file stats: {str(file_error)}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting taxonomy stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving hierarchy statistics")

# Quick search endpoint
@router.get("/search", response_model=dict)
async def search_taxonomy(
    query: str = Query(..., min_length=2, description="Search query"),
    field: str = Query("name", description="Field to search in"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum results"),
    max_depth: Optional[int] = Query(3, ge=1, le=10, description="Maximum search depth"),
    include_children: bool = Query(False, description="Include children in search results"),
    use_database: bool = Query(True, description="Use database search if available"),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
) -> JSONResponse:
    """
    Search taxonomy data for specific terms with hierarchical support
    """
    async with semaphore:
        try:
            if use_database:
                try:
                    # Try database search first
                    results = await taxonomy_manager.db_manager.search_taxonomy(
                        db=db,
                        query=query,
                        field=field,
                        limit=limit,
                        include_children=include_children
                    )
                    
                    search_response = {
                        "success": True,
                        "search": {
                            "query": query,
                            "field": field,
                            "results_count": len(results),
                            "source": "database"
                        },
                        "results": results,
                        "metadata": {
                            "timestamp": time.time(),
                            "cached": False
                        }
                    }
                    
                    return JSONResponse(content=search_response, status_code=200)
                    
                except Exception as db_error:
                    logger.warning(f"Database search failed, falling back to file: {str(db_error)}")
            
            # Fallback to file-based search
            result = await taxonomy_manager.get_paginated_data(
                file_name="taxonomy_outline.json",
                page=1,
                page_size=limit,
                search_query=query,
                search_field=field,
                max_depth=max_depth
            )

            # Restructure response for search
            search_response = {
                "success": True,
                "search": {
                    "query": query,
                    "field": field,
                    "max_depth": max_depth,
                    "results_count": len(result["data"]),
                    "source": "file"
                },
                "results": result["data"],
                "metadata": result["metadata"]
            }

            return JSONResponse(content=search_response, status_code=200)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in search: {str(e)}")
            raise HTTPException(status_code=500, detail="Search failed")

# Get taxonomy item by ID (database only)
@router.get("/item/{item_id}", response_model=dict)
async def get_taxonomy_item(
    item_id: int,
    include_children: bool = Query(True, description="Include children"),
    max_depth: Optional[int] = Query(None, ge=1, le=10, description="Maximum depth for children"),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
) -> JSONResponse:
    """Get a specific taxonomy item by database ID with its children"""
    try:
        with taxonomy_manager.db_manager.get_cursor(db) as cursor:
            cursor.execute("""
                SELECT id, taxonomy_id, name, description, parent_id, level, path, abstract, metadata,
                       created_at, updated_at
                FROM taxonomy_items 
                WHERE id = %s
            """, (item_id,))
            
            item = cursor.fetchone()
            
            if not item:
                raise HTTPException(status_code=404, detail="Taxonomy item not found")
            
            item_dict = dict(item)
            
            if include_children:
                children = await taxonomy_manager.db_manager._get_children(
                    db, item_id, max_depth
                )
                item_dict['children'] = children
                item_dict['children_count'] = len(children)
            
            return JSONResponse(
                content={
                    "success": True,
                    "data": item_dict,
                    "metadata": {
                        "timestamp": time.time(),
                        "source": "database"
                    }
                },
                status_code=200
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting taxonomy item: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving taxonomy item")

# Health check endpoint
@router.get("/health")
async def health_check():
    """Check if the taxonomy service is healthy"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": time.time(),
            "components": {}
        }
        
        # Check zip file
        try:
            if os.path.exists(ZIP_FILE_PATH):
                with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
                    zip_ref.testzip()
                health_status["components"]["zip_file"] = "healthy"
            else:
                health_status["components"]["zip_file"] = "file_not_found"
        except Exception as e:
            health_status["components"]["zip_file"] = f"error: {str(e)}"
        
        # Check database (if available)
        try:
            # This would require a database connection check
            health_status["components"]["database"] = "not_checked"
        except Exception as e:
            health_status["components"]["database"] = f"error: {str(e)}"
        
        # Check cache
        health_status["components"]["cache"] = {
            "status": "healthy",
            "size": len(cache),
            "keys": len(cache_timestamps)
        }
        
        # Determine overall status
        if any("error" in str(status) for status in health_status["components"].values()):
            health_status["status"] = "degraded"
            return JSONResponse(content=health_status, status_code=200)  # Still return 200 but indicate degraded
        
        return JSONResponse(content=health_status, status_code=200)
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": "unhealthy", 
                "error": str(e),
                "timestamp": time.time()
            },
            status_code=503
        )

# Cache management endpoints
@router.post("/cache/clear")
async def clear_cache(
    current_user: User = Depends(get_current_user)
):
    """Clear the API cache"""
    global cache, cache_timestamps
    
    cache_size_before = len(cache)
    cache.clear()
    cache_timestamps.clear()

    return JSONResponse(
        content={
            "success": True, 
            "message": "Cache cleared successfully",
            "cleared_entries": cache_size_before,
            "timestamp": time.time()
        },
        status_code=200
    )

@router.get("/cache/stats")
async def get_cache_stats(
    current_user: User = Depends(get_current_user)
):
    """Get cache statistics"""
    try:
        # Calculate cache stats
        total_entries = len(cache)
        valid_entries = sum(1 for key in cache.keys() if taxonomy_manager._is_cache_valid(key))
        expired_entries = total_entries - valid_entries
        
        # Memory estimation (rough)
        estimated_memory_kb = sum(
            len(json.dumps(value)) for value in cache.values()
        ) / 1024
        
        return JSONResponse(
            content={
                "total_entries": total_entries,
                "valid_entries": valid_entries,
                "expired_entries": expired_entries,
                "estimated_memory_kb": round(estimated_memory_kb, 2),
                "cache_ttl_seconds": CACHE_TTL,
                "timestamp": time.time()
            },
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving cache statistics")