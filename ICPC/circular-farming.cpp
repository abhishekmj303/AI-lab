#include <bits/stdc++.h>
using namespace std;
int main()
{
    cout << "Enter the coordinates of the field: " << endl;
    float ux, uy, lx, ly;
    cout << "Upper left (x y): ";
    cin >> ux >> uy;
    cout << "Lower right (x y): ";
    cin >> lx >> ly;

    float dx, dy;
    cout << "Enter the coordinates of the device: " << endl;
    cout << "Center (x y): ";
    cin >> dx >> dy;

    int n;
    cout << "Enter the number of trees: ";
    cin >> n;

    const int up = min({dx - ux, uy - dy, lx - dx, dy - ly});
    vector<bool> arr(up, true);
    cout << "Enter the coordinates and radius of the trees: " << endl;
    for (int i = 0; i < n; i++)
    {
        float x, y, r;
        cout << "Tree " << i + 1 << " (x y r): ";
        cin >> x >> y >> r;

        float d = sqrt((x - dx) * (x - dx) + (y - dy) * (y - dy));
        int ll = max(0, (int)ceil(d - r)), ul = (int)floor(d + r);
        if ((int)(d - r) == d - r)
            ll++;
        if ((int)(d + r) == d + r)
            ul--;
        for (int i = ll; i <= ul; i++)
        {
            if (i > up)
                break;
            arr[i - 1] = false;
        }
    }

    int cnt = 0;
    cout << "Number of complete crop rings: " << count(arr.begin(), arr.end(), true) << endl;
    return 0;
}
