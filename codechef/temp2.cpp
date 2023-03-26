#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <unordered_map>
#include <cmath>
#include <string>
#define int long long int
using namespace std;


int good_number(int n){
    int mod=1000000007;
    if(n==3){
        return 720;
    }
    return (9*good_number(n-1)-72)%mod;
}


void solve()
{
    int mod=1000000007;
    int n;
    cin>>n;
    if(n==1){
        cout<<9<<endl;
        return;
    }
    if(n==2){
        cout<<81<<endl;
        return;
    }
    
    cout<<good_number(n)<<endl;
    
    
    
    
}

int32_t main()
{
#ifndef ONLINE_MODE
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
#endif

    // int t;
    // cin >> t;
    // for (int _ = 0; _ < t; _++)
    // {
    //     solve();
    // }
    solve();
    return 0;
}
