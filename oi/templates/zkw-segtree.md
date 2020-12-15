<!--title: ZKW SegTree-->
<!--description: <del>I love ZKW</del>-->
<!--creationDate: 20201214-->

[Submit here](https://judge.yosupo.jp/problem/point_add_range_sum)

```cpp
// ZKW SegTree

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

#define DEPTH 19
#define MAXN (1 << DEPTH)

ll a[MAXN*2+10];

inline void build(){
    for(int i=MAXN-1;i;i--)a[i]=a[i*2]+a[i*2+1];
}

void Add(int x,ll val){
    x+=MAXN;
    a[x]+=val;
    for(x/=2;x;x/=2)a[x]+=val;
}

void Set(int x,ll val){
    Add(x,val-a[x+MAXN]);
}

ll query(int l,int r){
    ll ans=0;
    for(l=l+MAXN-1,r=r+MAXN+1;l^r^1;l/=2,r/=2){
        if(~l&1)ans+=a[l^1];
        if(r&1)ans+=a[r^1];
    }
    return ans;
}

int main() {
    ios_base::sync_with_stdio(false);
    int n, m;
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= n; i++) {
        scanf("%lld", a + MAXN + i);
    }
    build();
    for (int mm = 0; mm < m; mm++) {
        int ty;
        scanf("%d", &ty);
        if (ty == 0) {
            int x;
            ll val;
            scanf("%d%lld", &x, &val);
            x++;
            Add(x, val);
        } else {
            int l, r;
            scanf("%d%d", &l, &r);
            l++;
            printf("%lld\n", query(l, r));
        }
    }
    return 0;
}
```