from functools import cmp_to_key
from datetime import timedelta

def compare(a, b):
    if a['total_score'] > b['total_score']:
        return -1
    elif a['total_score'] < b['total_score']:
        return 1
    else:
        if a['total_seconds'] > b['total_seconds']:
            return 1
        elif a['total_seconds'] < b['total_seconds']:
            return -1
        else:
            return 0

def get_contest_leaderboard(contest):
    leaderboard = []

    for user in contest.users.all():
        subs = user.submission_set.filter(problem__contest=contest, is_final=True)
        total_score, total_seconds, sub_count = 0, 0, 0
        for sub in subs:
            sub_count += 1
            total_score += sub.judge_score
            total_seconds += sub.contest_start_timedelta().total_seconds()
        
        if sub_count: total_seconds /= sub_count
        
        total_time = str(timedelta(seconds=round(total_seconds)))

        leaderboard.append({
            'user': user,
            'final_subs': subs,
            'total_score': total_score,
            'total_seconds': total_seconds,
            'total_time': total_time,
        })
    
    leaderboard.sort(key=cmp_to_key(compare))
    return leaderboard