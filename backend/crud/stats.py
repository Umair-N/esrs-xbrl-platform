from psycopg2.extras import RealDictCursor

class StatsCRUD:
    def get_user_stats(self, db) -> dict:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
            SELECT 
                COUNT(*) FILTER (
                    WHERE DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE)
                ) AS users_added_this_month,
                
                COUNT(*) FILTER (
                    WHERE DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
                ) AS users_added_last_month,
                
                COUNT(*) FILTER (WHERE platform_access = TRUE) AS platform_access_true,
                COUNT(*) FILTER (WHERE platform_access = FALSE) AS platform_access_false,
                
                COUNT(*) FILTER (
                    WHERE DATE_TRUNC('day', last_accessed_at) = DATE_TRUNC('day', CURRENT_DATE)
                ) AS last_accessed_today,
                
                COUNT(*) FILTER (
                    WHERE DATE_TRUNC('day', last_accessed_at) = DATE_TRUNC('day', CURRENT_DATE - INTERVAL '1 day')
                ) AS last_accessed_yesterday,
                
                COUNT(*) AS total
            FROM users;
            """
            cursor.execute(query)
            result = cursor.fetchone()

            total = result["total"]
            this_month = result["users_added_this_month"] or 0
            last_month = result["users_added_last_month"] or 0
            platform_access_true = result["platform_access_true"] or 0
            platform_access_false = result["platform_access_false"] or 0
            last_accessed_today = result["last_accessed_today"] or 0
            last_accessed_yesterday = result["last_accessed_yesterday"] or 0

            # User growth percentage
            if last_month == 0:
                change_percentage = 100.0 if this_month > 0 else 0.0
            else:
                change_percentage = ((this_month - last_month) / last_month) * 100

            # Daily access change percentage
            if last_accessed_yesterday == 0:
                access_change_percentage = 100.0 if last_accessed_today > 0 else 0.0
            else:
                access_change_percentage = ((last_accessed_today - last_accessed_yesterday) / last_accessed_yesterday) * 100

            return {
                "total": total,
                "this_month": this_month,
                "last_month": last_month,
                "change_percentage": round(change_percentage, 2),
                "platform_access_true": platform_access_true,
                "platform_access_false": platform_access_false,
                "last_accessed_today": last_accessed_today,
                "last_accessed_yesterday": last_accessed_yesterday,
                "access_change_percentage": round(access_change_percentage, 2)
            }
        finally:
            cursor.close()

stats_crud = StatsCRUD()
