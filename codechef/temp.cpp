#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <unordered_map>
#include <cmath>
#include <string>
#define int long long int
using namespace std;

int search_j(int arr[], int n, int x, int j)
{
    for (int i = j; i < n; i++)
    {
        if (arr[i] == x)
        {
            return i;
        }
    }
}

void print_pair(int i, int j)
{
    cout << i << " " << j<<endl;
    cout << j << " " << i<<endl;
    cout << i << " " << j<<endl;
    return;
}

void solve()
{
    int n;
    cin >> n;
    int arr[n];
    int temp[n];
    unordered_map<int,int> mp;

    for (int i = 0; i < n; i++)
    {
        cin >> arr[i];
        mp[arr[i]]=i;
        temp[i] = arr[i];
    }
    stable_sort(temp, temp + n);
    int cnt = 0;
    string out = "";
    int out1[n];
    int out2[n];
    for (int i = 0; i < n; i++)
    {
        int idx = mp[temp[i]];
        if (idx != i)
        {

            // print_pair(i,idx);
            out1[cnt]=i;out2[cnt]=idx;
            cnt++;
            swap(arr[i], arr[idx]);
            swap(mp[arr[i]],mp[arr[idx]]);

            // cnt += 1;
        }
    }
    cout << (3*cnt) << endl;
    for (int i = 0; i < cnt; i++)
    {
        print_pair(out1[i]+1,out2[i]+1);
    }
    
}

int32_t main()
{
#ifndef ONLINE_MODE
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
#endif

    int t;
    cin >> t;
    for (int _ = 0; _ < t; _++)
    {
        solve();
    }

    return 0;
}
