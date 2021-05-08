<!--title: Zzzyt's New Template-->
<!--description: Much more functionality!-->
<!--creationDate: 2020-12-14-->

# Code

```cpp
/*
Code by Zzzyt

Problem: 
Algorithm: 
Status: 
Date: 
Version: 1
*/

#include <algorithm>
#include <deque>
#include <iostream>
#include <map>
#include <math.h>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <time.h>
#include <utility>
#include <vector>
// #include <chrono>
// #include <random>

using namespace std;

#define popc(x) __builtin_popcount(x)
#define over(x)        \
    {                  \
        printf(x);     \
        putchar('\n'); \
        exit(0);       \
    }
#define all(x) x.begin(), x.end()
#define ceil(a, b) ((a - 1) / b + 1)
#define srand() srand(time(0))
#define srandx() mt19937 rng(chrono::steady_clock::now().time_since_epoch().count())
#define randx(l, r) uniform_int_distribution<int>(l, r)(rng)
#define pii pair<int, int>
#define nosync ios::sync_with_stdio(0)
#define pb push_back
typedef long long ll;
typedef unsigned long long ull;

inline int fread() {
    char ch = getchar();
    int x = 0, f = 1;
    while (ch < '0' || ch > '9') {
        if (ch == '-')
            f = -1;
        ch = getchar();
    }
    while (ch >= '0' && ch <= '9') {
        x = x * 10 + ch - '0';
        ch = getchar();
    }
    return x * f;
}

template <typename T1, typename T2>
ostream &operator<<(ostream &os, const pair<T1, T2> &ptt) {
    os << "(" << ptt.first << ", " << ptt.second << ")";
    return os;
}

template <typename T>
ostream &operator<<(ostream &os, const vector<T> &vt) {
    os << "{";
    for (int i = 0; i < vt.size() - 1; i++) {
        os << vt[i] << ", ";
    }
    os << vt[vt.size() - 1] << "}";
    return os;
}

/* -------- End of Template -------- */

#define INF 1000000007

int main(int argc, char *argv[]) {
    cin.tie(0);
    //freopen(".in", "r", stdin);
#ifndef ZZZYT
    //freopen(".out", "w", stdout);
#endif
    
    return 0;
}
```
