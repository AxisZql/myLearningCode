#include<iostream>
#include<vector>
#include<stack>
using namespace std;

vector<int> nextGreaterElements(vector<int>& nums){
    int n=nums.size();
    vector<int> ans(n,-1);//初始化保存答案的数据
    stack<int> stk;//stk是用来记录入栈元素原来的下标
    for(int i=0;i<n*2-1;++i){
        while(!stk.empty()&&nums[stk.top()]<nums[i%n])
        {
            ans[stk.top()]=nums[i%n];
            stk.pop();
        }
        stk.push(i%n);
    }
  return ans;
}

int main(){

}
