
from settings import Settings
from game_stats import GameStats


ai_settings = Settings()
a = GameStats(ai_settings)
b = a.return_high_score()
print(b)
