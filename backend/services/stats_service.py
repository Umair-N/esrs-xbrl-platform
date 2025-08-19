from crud.stats import stats_crud 
class StatsService:
    def get_stats (self, db) -> dict:
        return stats_crud.get_user_stats(db)

stats_service = StatsService()