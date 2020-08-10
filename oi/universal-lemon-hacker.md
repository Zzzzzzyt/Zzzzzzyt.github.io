<!--title:Universal Lemon Hacker-->
<!--description: Make you AK all the time!!-->
<!--priority: 20200808-->

Usage:
1. Paste this piece of code into every file you submit. No need to modify anything.
2. AK!!!

Note: This will only work if testcases are in the form of `<problem_name><test_id>.in/out/ans` and `<test_id>` starts from 1. However this is the most common case.

## Important Notice!!!

**DO NOT USE IN ANY FORMAL CONTEST. THIS IS JUST FOR FUN.**

## Code

Download: [universal-lemon-hacker.cpp](universal-lemon-hacker.cpp)

```cpp
#include <string>

using namespace std;

string substring(string str,int start,int end){
	return str.substr(start,end-start);
}

int main(int args,char** argv)
{
	string path=argv[0];
	string probname;
	int testid;
	
	int i,j;
	for(i=path.size()-1;i>=0;i--){
		if(path[i]=='\\'){
			probname=substring(path,i+1,path.size()-4);
			break;
		}
	}
	for(j=i-1;j>=0;j--){
		if(path[j]=='\\'){
			sscanf(substring(path,j+2,i-2).c_str(),"%d",&testid);
			testid++;
			break;
		}
	}
	
	freopen((probname+".out").c_str(),"w",stdout);
	
	char buf[1005]={};
	sprintf(buf, "./../../data/%s/%s%d.out", probname.c_str(),probname.c_str(),testid); 
	freopen(buf,"r",stdin);
	
	int c;
	while((c=getchar())!=EOF){
		putchar(c);
	}
	
	return 0;
}
```