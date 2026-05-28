import pandas as pd
import numpy as np

def generate_analytics(tasks):
    # 🚀 FIX: Safety check if there are no tasks yet
    if not tasks:
        return {
            "total": 0,
            "completed": 0,
            "pending": 0,
            "percentage": 0.0
        }

    data = []
    for task in tasks:
        data.append({
            "status": task.status
        })

    df = pd.DataFrame(data)

    total = len(df)
    completed = len(df[df['status'] == 'Completed'])
    pending = len(df[df['status'] == 'Pending'])

    percentage = 0
    if total > 0:
        percentage = np.round((completed / total) * 100, 2)

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "percentage": percentage
    }
