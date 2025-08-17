"use client"

import { useState, useMemo } from "react"

export interface PaginationData {
    total: number
    page: number
    pages: number
    limit: number
}

export interface UsePaginationOptions {
    initialPage?: number
    initialLimit?: number
}

export interface UsePaginationReturn {
    currentPage: number
    limit: number
    setPage: (page: number) => void
    setLimit: (limit: number) => void
    nextPage: () => void
    previousPage: () => void
    goToFirstPage: () => void
    goToLastPage: (totalPages: number) => void
    canGoNext: (totalPages: number) => boolean
    canGoPrevious: boolean
    getPageNumbers: (totalPages: number, maxVisible?: number) => (number | "...")[]
}

export const usePagination = ({
    initialPage = 1,
    initialLimit = 10,
}: UsePaginationOptions = {}): UsePaginationReturn => {
    const [currentPage, setCurrentPage] = useState(initialPage)
    const [limit, setLimit] = useState(initialLimit)

    const setPage = (page: number) => {
        if (page >= 1) {
            setCurrentPage(page)
        }
    }

    const nextPage = () => setPage(currentPage + 1)
    const previousPage = () => setPage(currentPage - 1)
    const goToFirstPage = () => setPage(1)
    const goToLastPage = (totalPages: number) => setPage(totalPages)

    const canGoNext = (totalPages: number) => currentPage < totalPages
    const canGoPrevious = currentPage > 1

    const getPageNumbers = useMemo(() => {
        return (totalPages: number, maxVisible = 5): (number | "...")[] => {
            if (totalPages <= maxVisible) {
                return Array.from({ length: totalPages }, (_, i) => i + 1)
            }

            const pages: (number | "...")[] = []
            const halfVisible = Math.floor(maxVisible / 2)

            if (currentPage <= halfVisible + 1) {
                // Show first pages
                for (let i = 1; i <= maxVisible - 1; i++) {
                    pages.push(i)
                }
                pages.push("...")
                pages.push(totalPages)
            } else if (currentPage >= totalPages - halfVisible) {
                // Show last pages
                pages.push(1)
                pages.push("...")
                for (let i = totalPages - maxVisible + 2; i <= totalPages; i++) {
                    pages.push(i)
                }
            } else {
                // Show middle pages
                pages.push(1)
                pages.push("...")
                for (let i = currentPage - halfVisible + 1; i <= currentPage + halfVisible - 1; i++) {
                    pages.push(i)
                }
                pages.push("...")
                pages.push(totalPages)
            }

            return pages
        }
    }, [currentPage])

    return {
        currentPage,
        limit,
        setPage,
        setLimit,
        nextPage,
        previousPage,
        goToFirstPage,
        goToLastPage,
        canGoNext,
        canGoPrevious,
        getPageNumbers,
    }
}
