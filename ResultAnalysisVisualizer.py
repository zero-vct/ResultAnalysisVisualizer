import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class ResultAnalysisVisualizer:
    def __init__(self, data):
        self.data = data

    # 过滤数据，包含主队和客队的比赛
    def filter_data(self, home_team, away_team):
        filtered_data = self.data[
            (self.data['Match'].str.contains(home_team)) & 
            (self.data['Match'].str.contains(away_team))
        ]
        return filtered_data
    
    def WinRateChart(self, home_team, away_team):
        filtered_data = self.filter_data(home_team, away_team)
        
        # 提取比赛信息
        home_wins, away_wins, draws = 0, 0, 0
        
        for _, row in filtered_data.iterrows():
            match = row['Match']
            score = row['Score']
            
            # 解析球队和比分
            teams = match.split(':')
            scores = score.strip().split(':')
            score_home, score_away = int(scores[0]), int(scores[1])
            
            if home_team in teams[0]:
                if score_home > score_away:
                    home_wins += 1
                elif score_home < score_away:
                    away_wins += 1
                else:
                    draws += 1
            else:
                if score_home < score_away:
                    home_wins += 1
                elif score_home > score_away:
                    away_wins += 1
                else:
                    draws += 1

        # 制作饼图
        labels = ['{} Wins'.format(home_team), '{} Wins'.format(away_team), 'Draws']
        sizes = [home_wins, away_wins, draws]
        colors = ['gold', 'lightcoral', 'lightskyblue']
        explode = (0.1, 0, 0)  # 突出显示第一块（主队胜利）

        plt.figure()
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=140)
        plt.title(f"Win Rate Chart: {home_team} vs {away_team}")
        plt.axis('equal')

    def ScoreDistributionChart(self, home_team, away_team):
        filtered_data = self.filter_data(home_team, away_team)
        
        home_scores = []
        away_scores = []
        
        for _, row in filtered_data.iterrows():
            match = row['Match']
            score = row['Score']
            
            teams = match.split(':')
            scores = score.strip().split(':')
            score_home, score_away = int(scores[0]), int(scores[1])
            
            if home_team in teams[0]:
                home_scores.append(score_home)
                away_scores.append(score_away)
            else:
                home_scores.append(score_away)
                away_scores.append(score_home)
        
        # 创建一个得分分布矩阵
        max_score = max(max(home_scores), max(away_scores))
        score_matrix = np.zeros((max_score + 1, max_score + 1))

        for h_score, a_score in zip(home_scores, away_scores):
            score_matrix[h_score, a_score] += 1
        
        plt.figure()
        sns.heatmap(score_matrix, annot=True, fmt=".0f", cmap="YlGnBu")
        plt.title(f"Score Distribution: {home_team} vs {away_team}")
        plt.xlabel(f"{away_team} Scores")
        plt.ylabel(f"{home_team} Scores")

    def DiffGoalFrequencyChart(self, home_team, away_team):
        filtered_data = self.filter_data(home_team, away_team)
        
        goal_diffs = []
        
        for _, row in filtered_data.iterrows():
            match = row['Match']
            score = row['Score']
            
            teams = match.split(':')
            scores = score.strip().split(':')
            score_home, score_away = int(scores[0]), int(scores[1])
            
            if home_team in teams[0]:
                goal_diff = score_home - score_away
            else:
                goal_diff = score_away - score_home

            goal_diffs.append(goal_diff)
        
        plt.figure()
        plt.hist(goal_diffs, bins=range(min(goal_diffs), max(goal_diffs) + 2), edgecolor='black')
        plt.title(f"Goal Difference Frequency: {home_team} vs {away_team}")
        plt.xlabel('Goal Difference')
        plt.ylabel('Frequency')

    def ScoreFrequencyChart(self, home_team, away_team):
        filtered_data = self.filter_data(home_team, away_team)
        
        home_scores = []
        away_scores = []
        
        for _, row in filtered_data.iterrows():
            match = row['Match']
            score = row['Score']
            
            teams = match.split(':')
            scores = score.strip().split(':')
            score_home, score_away = int(scores[0]), int(scores[1])
            
            if home_team in teams[0]:
                home_scores.append(score_home)
                away_scores.append(score_away)
            else:
                home_scores.append(score_away)
                away_scores.append(score_home)
        
        plt.figure()
        plt.hist([home_scores, away_scores], bins=range(0, max(max(home_scores), max(away_scores)) + 2), 
                 label=[home_team, away_team], edgecolor='black', alpha=0.7)
        plt.title(f"Score Frequency: {home_team} vs {away_team}")
        plt.xlabel('Goals')
        plt.ylabel('Frequency')
        plt.legend()