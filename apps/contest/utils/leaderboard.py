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

    for user in contest.participants.all():
        # Only CONTEST front-end submissions
        subs = user.submission_frontendsubmissions.filter(
            frontendcontestsubmission__contest=contest,
            frontendcontestsubmission__is_final=True
        )

        total_score, total_seconds, sub_count = 0, 0, 0
        for sub in subs:
            sub_count += 1
            total_score += sub.judge_score
            total_seconds += sub.frontendcontestsubmission.contest_start_timedelta().total_seconds()
        
        if sub_count: total_seconds /= sub_count
        
        total_time = str(timedelta(seconds=round(total_seconds)))
        
        final_subs = []
        for problem in contest.problems.all():
            appended = False
            for sub in subs:
                if sub.problem == problem:
                    final_subs.append(sub)
                    appended = True
                    break
            if not appended:
                final_subs.append(None)
        
        leaderboard.append({
            'user': user,
            'final_subs': final_subs,
            'total_score': total_score,
            'total_seconds': total_seconds,
            'total_time': total_time,
        })
    
    leaderboard.sort(key=cmp_to_key(compare))
    return leaderboard