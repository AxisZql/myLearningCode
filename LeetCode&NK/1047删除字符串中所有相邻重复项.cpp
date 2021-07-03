#include<iostream>
#include<vector>
#include<string>
using namespace std;

/*
由于 std::string 类本身就提供了类似「入栈」和「出栈」
的接口，因此我们直接将需要被返回的字符串作为栈即可
*/
class Solution{
    public:
    string removeDuplicates(string S){
        string stk;
        for(char ch:S){
            if(!stk.empty()&&stk.back()==ch){
                stk.pop_back();//删除stk的最后一个元素，相当于出栈
            }
            else{
                stk.push_back(ch);
            }
        }
        return stk;

    }
};



int main(){

}
