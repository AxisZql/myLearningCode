#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

/*
思路：1.组成套娃信封的元素中其w和h一定不能都出现在其他信封的元素中。
2.答案信封的每一个w和h都不一样

官方解法：看不懂！！！

*/

class Solution {
public:
    int maxEnvelopes(vector<vector<int>>& envelopes) {
        if (envelopes.empty()) {
            return 0;
        }
        
        int n = envelopes.size();
        sort(envelopes.begin(), envelopes.end(), [](const auto& e1, const auto& e2) {
            return e1[0] < e2[0] || (e1[0] == e2[0] && e1[1] > e2[1]);//前一个元素w大于后一个元素的w或者
            //相邻两个元素的w相等而且前面元素的h大于后面元素的h则把它们按照递增的方式交换位置
        });

        vector<int> f(n, 1);
        for (int i = 1; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                if (envelopes[j][1] < envelopes[i][1]) {
                    f[i] = max(f[i], f[j] + 1);
                }
            }
        }
        return *max_element(f.begin(), f.end());
    }
};


int main()
{

}