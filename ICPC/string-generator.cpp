#include <bits/stdc++.h>
using namespace std;
bool check(string &s, string &m, int i, int st, int end)
{
    if (i == -1)
    {
        return true;
    }
    if (s[i] == m[st] && s[i] == m[end])
    {
        return check(s, m, i - 1, st + 1, end) || check(s, m, i - 1, st, end - 1);
    }
    else if (s[i] == m[st])
    {
        return check(s, m, i - 1, st + 1, end);
    }
    else if (s[i] == m[end])
    {
        return check(s, m, i - 1, st, end - 1);
    }
    else
    {
        return false;
    }
}

int main()
{
    int l = 0;
    cout << "Enter the length of the string: ";
    cin >> l;

    string s;
    string m;
    cout << "Enter the string you have: ";
    cin >> s;
    cout << "Enter the string you want to generate: ";
    cin >> m;

    cout << "Can the string be generated? ";
    if (check(s, m, l - 1, 0, l - 1))
    {
        cout << "YES\n";
    }
    else
    {
        cout << "NO\n";
    }
}
