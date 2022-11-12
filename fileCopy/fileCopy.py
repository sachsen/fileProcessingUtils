import glob
import os.path
import platform
import shutil
#from smb.SMBConnection import SMBConnection

#Copy情報
class CopyOp():
    #*:任意の文字列
    #?:任意の１文字
    #[abc]又は[a-z]:括弧内のいずれかの文字
    #ワイルドカードはパスの途中のディレクトリにも有効
    def __init__(self,copyFromRoot=None,copyFromChileDirs=[],copyToRoot=None):
        self.copyFromRoot=copyFromRoot
        self.copyFromChildDirs=copyFromChileDirs
        self.copyToRoot=copyToRoot
        self.fileList = []
        pass

    # コピーディレクトリが設定されているか？
    def checkSetting(self,output=True):
        message=""
        result=True
        if self.copyToRoot is None:
            message="no copyToRoot"
            result= False
        elif self.copyFromRoot is None:
            message="no copyFromRoot"
            result= False
        elif len(self.copyFromChildDirs)==0:
            message="no copyFromChildDirs"
            result= False
        elif not os.path.exists(self.copyFromRoot):
            message = "not exist copyFromRoot"
            result= False
        if not result:
            if output:
                print(message)
            return result
        return True

    def fetchFileList(self,output=True):
        if not self.checkSetting(output=output):
            return False

        for path in self.copyFromChildDirs:
            path_abs=os.path.join(self.copyFromRoot,path)
            paths=glob.glob(path_abs)
            paths2=[]
            for p in paths:
                path_rel=os.path.relpath(p,self.copyFromRoot)
                paths2.append([p,path_rel])
            self.fileList.extend(paths2)

        return True

    def copyFile(self,output=True):
        if not self.fetchFileList(output=output):
            if output:
                print("not copied")
            return
        if not os.path.exists(self.copyToRoot):# 存在しない場合は作成
            os.makedirs(self.copyToRoot, exist_ok=True)
        for paths in self.fileList:
            path_abs,path_rel=paths
            copy2path=os.path.join(self.copyToRoot,path_rel)
            os.makedirs(os.path.dirname(copy2path), exist_ok=True)
            shutil.copy2(path_abs,copy2path)



