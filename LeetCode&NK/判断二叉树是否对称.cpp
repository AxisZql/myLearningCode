#include<iostream>
using namespace std;

struct TreeNode {
int val;
struct TreeNode *left;
struct TreeNode *right;
};

class Solution {
public:
    /**
     * 
     * @param root TreeNode类 
     * @return bool布尔型
     */
    bool isSymmetric(TreeNode* root) {
        // write code here
        if(root==NULL){
            return true;
        }
        return compare(root->left,root->right);
    }
    bool compare(TreeNode*lchild,TreeNode*rchild){
        if(lchild==NULL&&rchild==NULL){
            return true;
        }
        else if(lchild==NULL||rchild==NULL||lchild->val==!rchild->val);
        {
            return false;
        }
        return compare(lchild->left,rchild->right)&&compare(lchild->right,rchild->left);
    }
};
