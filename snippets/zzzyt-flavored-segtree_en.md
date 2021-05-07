<!--title: Zzzyt Flavored Segment Tree-->
<!--description: A weird power-of-two implmentation of the segment tree.-->
<!--creationDate: 20200810-->

# Code

This one is range sum, range add version.

```cpp
/*
Zzzyt Flavored Power-of-two Segment Tree
*/

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <ctime>
#include <deque>
#include <iostream>
#include <list>
#include <map>
#include <memory.h>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <stdio.h>
#include <string.h>
#include <string>
#include <utility>
#include <vector>

using namespace std;

#define INF 1000000007
#define popc(x) __builtin_popcount(x)
#define pii pair<int, int>
#define piii pair<int, pair<int, int>>
#define mp make_pair
#define pb push_back
typedef long long ll;

#define DEPTH 17
#define MAXN (1 << DEPTH)

ll a[MAXN * 2 + 10];
ll tag[MAXN + 10];

inline void pushdown(int x, int l, int r) {
    if (tag[x]) {
        if (x < MAXN / 2) {
            tag[x * 2] += tag[x];
            tag[x * 2 + 1] += tag[x];
        }
        a[x * 2] += tag[x] * (r - l) / 2;
        a[x * 2 + 1] += tag[x] * (r - l) / 2;
        tag[x] = 0;
    }
}

ll query(int L, int R, int x = 1, int l = 0, int r = MAXN) {
    if (l == L && r == R)
        return a[x];
    pushdown(x, l, r);
    int mid = (l + r) / 2;
    ll ret = 0;
    if (L < mid)
        ret += query(L, min(mid, R), x * 2, l, mid);
    if (R > mid)
        ret += query(max(mid, L), R, x * 2 + 1, mid, r);
    return ret;
}

void add(int L, int R, ll val, int x = 1, int l = 0, int r = MAXN) {
    a[x] += val * (R - L);
    if (l == L && r == R) {
        tag[x] += val;
        return;
    }
    int mid = (l + r) / 2;
    if (L < mid)
        add(L, min(mid, R), val, x * 2, l, mid);
    if (R > mid)
        add(max(mid, L), R, val, x * 2 + 1, mid, r);
}

void build() {
    for (int i = MAXN - 1; i; i--) {
        a[i] = a[i * 2] + a[i * 2 + 1];
    }
}

int main() {
    int n, m;
    scanf("%d%d", &n, &m);
    for (int i = 0; i < n; i++) {
        scanf("%lld", a + MAXN + i);
    }
    build();
    for (int mm = 0; mm < m; mm++) {
        int ty;
        scanf("%d", &ty);
        if (ty == 1) {
            int l, r;
            ll val;
            scanf("%d%d%lld", &l, &r, &val);
            l--;
            add(l, r, val);
        } else {
            int l, r;
            scanf("%d%d", &l, &r);
            l--;
            printf("%lld\n", query(l, r));
        }
    }
    return 0;
}
```
