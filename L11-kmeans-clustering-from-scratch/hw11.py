import numpy as np
import matplotlib.pyplot as plt

# הגדרת פרמטרים
n_total = 6000  # סה"כ נקודות
n_clusters = 3
n_per_cluster = n_total // n_clusters  # 2000 נקודות לכל קלאסטר

# חישוב כמות נקודות
n_unique_per_cluster = int(n_per_cluster * 2/3)  # 1333 נקודות ייחודיות לכל קלאסטר
n_shared = n_total - (n_unique_per_cluster * n_clusters)  # 2001 נקודות משותפות

print(f"=== תכנון הדאטה ===")
print(f"נקודות ייחודיות לכל קלאסטר: {n_unique_per_cluster}")
print(f"נקודות משותפות לכל 3 הקלאסטרים: {n_shared}")
print(f"סה\"כ נקודות: {n_unique_per_cluster * n_clusters + n_shared}")

# הגדרת מרכזים לשלושת הקלאסטרים
centers = np.array([
    [0, 0],      # קלאסטר 1
    [5, 5],      # קלאסטר 2
    [10, 0]      # קלאסטר 3
])

# הגדרת שונות
std_unique = 1.0  # שונות לנקודות ייחודיות
std_shared = 2.5  # שונות גדולה יותר לנקודות משותפות

# יצירת הנקודות
np.random.seed(42)

# שלב 1: יצירת נקודות ייחודיות לכל קלאסטר
cluster1_unique = np.random.normal(centers[0], std_unique, (n_unique_per_cluster, 2))
cluster2_unique = np.random.normal(centers[1], std_unique, (n_unique_per_cluster, 2))
cluster3_unique = np.random.normal(centers[2], std_unique, (n_unique_per_cluster, 2))

# שלב 2: יצירת נקודות משותפות - במרכז הגיאומטרי של 3 הקלאסטרים
center_of_all = np.mean(centers, axis=0)
shared_points = np.random.normal(center_of_all, std_shared, (n_shared, 2))

# שלב 3: בניית המערך המלא
# כל נקודה תופיע 1 או 3 פעמים
X_list = []
true_labels_list = []  # התוויות האמיתיות

# הוספת נקודות ייחודיות
X_list.append(cluster1_unique)
true_labels_list.extend([0] * n_unique_per_cluster)

X_list.append(cluster2_unique)
true_labels_list.extend([1] * n_unique_per_cluster)

X_list.append(cluster3_unique)
true_labels_list.extend([2] * n_unique_per_cluster)

# הוספת נקודות משותפות - כל נקודה תופיע 3 פעמים!
X_list.append(shared_points)
true_labels_list.extend([0] * n_shared)  # שייכת לקלאסטר 0

X_list.append(shared_points)
true_labels_list.extend([1] * n_shared)  # גם לקלאסטר 1

X_list.append(shared_points)
true_labels_list.extend([2] * n_shared)  # גם לקלאסטר 2

# איחוד הכל
X = np.vstack(X_list)
true_labels = np.array(true_labels_list)

print(f"\n=== מערך הנתונים הסופי ===")
print(f"סה\"כ רשומות (כולל כפילויות): {len(X)}")
print(f"נקודות ייחודיות ממשיות: {n_unique_per_cluster * 3 + n_shared}")

# ===== מימוש K-means ידני =====
def kmeans(X, k=3, max_iters=100):
    """מימוש אלגוריתם K-means"""
    n_samples = X.shape[0]
    
    # אתחול מרכזים אקראיים
    random_indices = np.random.choice(n_samples, k, replace=False)
    centers = X[random_indices].copy()
    
    for iteration in range(max_iters):
        # חישוב מרחקים
        distances = np.zeros((n_samples, k))
        for i in range(k):
            distances[:, i] = np.sqrt(np.sum((X - centers[i])**2, axis=1))
        
        # שיוך לקלאסטר הקרוב ביותר
        labels = np.argmin(distances, axis=1)
        
        # עדכון מרכזים
        new_centers = np.zeros((k, X.shape[1]))
        for i in range(k):
            cluster_points = X[labels == i]
            if len(cluster_points) > 0:
                new_centers[i] = cluster_points.mean(axis=0)
            else:
                new_centers[i] = centers[i]
        
        # בדיקת התכנסות
        if np.allclose(centers, new_centers, rtol=1e-6):
            print(f"K-means התכנס אחרי {iteration + 1} איטרציות")
            break
        
        centers = new_centers
    
    # חישוב inertia
    inertia = 0
    for i in range(k):
        cluster_points = X[labels == i]
        inertia += np.sum((cluster_points - centers[i])**2)
    
    return labels, centers, inertia


# הרצת K-means
print("\n=== הרצת K-means ===")
kmeans_labels, centers_kmeans, inertia = kmeans(X, k=3, max_iters=100)

# ויזואליזציה
fig = plt.figure(figsize=(18, 5))

# גרף 1: התוויות האמיתיות (כולל הכפילויות)
plt.subplot(1, 3, 1)
scatter1 = plt.scatter(X[:, 0], X[:, 1], c=true_labels, cmap='viridis', 
                       alpha=0.5, s=20)
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=300, marker='X', 
            edgecolors='black', linewidths=2, label='מרכזים מקוריים')
plt.title(f'התוויות האמיתיות\n({n_shared} נקודות מופיעות פי 3)')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.colorbar(scatter1, label='קלאסטר אמיתי')
plt.grid(True, alpha=0.3)

# גרף 2: תוצאות K-means
plt.subplot(1, 3, 2)
scatter2 = plt.scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap='plasma', 
                       alpha=0.6, s=20)
plt.scatter(centers_kmeans[:, 0], centers_kmeans[:, 1], 
           c='red', s=300, marker='X', 
           edgecolors='black', linewidths=2, label='מרכזי K-means')
plt.title('תוצאות K-means')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.colorbar(scatter2, label='קלאסטר K-means')
plt.grid(True, alpha=0.3)

# גרף 3: השוואה
plt.subplot(1, 3, 3)
plt.scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap='plasma', 
           alpha=0.4, s=20)
plt.scatter(centers[:, 0], centers[:, 1], c='blue', s=300, 
           marker='X', edgecolors='black', linewidths=3, 
           label='מרכזים מקוריים', zorder=5)
plt.scatter(centers_kmeans[:, 0], centers_kmeans[:, 1], 
           c='red', s=250, marker='o', 
           edgecolors='black', linewidths=3, 
           label='מרכזי K-means', zorder=5)
plt.title('השוואה: מקורי vs K-means')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# סטטיסטיקות
print("\n=== סטטיסטיקות K-means ===")
print(f"Inertia: {inertia:.2f}")
print(f"\nגודל כל קלאסטר (כולל כפילויות):")
unique, counts = np.unique(kmeans_labels, return_counts=True)
for cluster_id, count in zip(unique, counts):
    print(f"  קלאסטר {cluster_id}: {count} רשומות ({count/len(X)*100:.1f}%)")

print("\nמרכזי הקלאסטרים שנמצאו:")
for i, center in enumerate(centers_kmeans):
    print(f"  קלאסטר {i}: [{center[0]:.2f}, {center[1]:.2f}]")
    
print("\nמרכזים מקוריים:")
for i, center in enumerate(centers):
    print(f"  קלאסטר {i}: [{center[0]:.2f}, {center[1]:.2f}]")