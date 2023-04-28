#include <bits/stdc++.h>
using namespace std;
int main()
{
    const int mod = 998244353;

    int n;
    cout << "Enter the length of the array: ";
    cin >> n;

    long long ans = 0;

    vector<int> A(n);
    cout << "Enter the array: ";
    for (int i = 0; i < n; ++i)
        cin >> A[i];
    
    for (int i = 0; i < n - 1; ++i)
    {
        int mi = min(A[i], A[i + 1]), smi = max(A[i], A[i + 1]);
        ans += (mi ^ smi);
        for (int j = i + 2; j < n; ++j)
        {
            if (A[j] <= mi)
            {
                smi = mi;
                mi = A[j];
            }
            else if (A[j] < smi)
                smi = A[j];
            ans += (mi ^ smi);
        }
    }
    cout << "Sum of the beauty values for all the subarrays: " << ans << '\n';
    return 0;
}