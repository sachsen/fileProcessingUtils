
import platform
from smb.SMBConnection import SMBConnection

#情報体
class CopyOp():
    #*:任意の文字列
    #?:任意の１文字
    #[abc]又は[a-z]:括弧内のいずれかの文字
    def __init__(self,copyFromRoot=None,copyFromChileDirs=[],copyToRoot=None):
        self.copyFromRoot=copyFromRoot
        self.copFromChildDirs=copyFromChileDirs
        self.copyToRoot=copyToRoot
        pass

def fileCopy():

    pass


if __name__ == '__main__':
    cp=CopyOp()
    cp.copyToRoot=r"H:\Data\20221011"
    cp.copyFromRoot=r"\\fennel\FullCap12\ExtraExperiment\ExtraExperiment20191201"
    cp.copFromChildDirs.append("")
    fileCopy()
    pass