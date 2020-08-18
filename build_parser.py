import json,urllib,os,sys
class Builder:
    def __init__(self):
        self.helptext='''利用Python3编写的基于JSON的软件打包器，类似于ArchLinux的PKGBUILD
用法: fbuild [命令] 参数
命令:
    build - 构建当前目录下的程序并制成软件包，若后面指定文件名则将FBUILD指定为该文件
    clean - 清理当前目录下除FBUILD外的所有文件
    help - 输出帮助信息
    info - 输出软件包信息，若后面指定文件名也会将FBUILD指定为该文件

fbuild用于将软件包从源代码打包为软件包，在这期间会检查依赖，并从Internet下载所需要的软件源码。
fbuild需要一个C/C++编译器(如clang/gcc)，以及GNU Make和tar,xz用于构建二进制ELF和打包。
    '''
        
    def entry(self,args):
        if len(args)==1:
            print(self.helptext)
        elif len(args)>=2:
            if args[1]=='help':
                print(self.helptext)
            elif args[1]=='build':
                if len(args)>2:
                    self.build(args[2])
                else:
                    self.build("FBUILD")
            elif args[1]=='clean':
                pass
            elif args[1]=='info':
                names=["Package Name","Version","Release","Branch","Maintainer","License","Architecture","Dependencies","Target"]
                index=0
                infofile="FBUILD"
                if len(args)>2:
                    infofile=args[2]
                for text in self.readinfo(infofile):
                    print("%s: %s"%(names[index],text))
                    index+=1
            else:
                print(f'无此命令，若需要帮助请执行"{args[0]} help"')
    def readinfo(self,filename):
        #对输入的JSON信息进行解析
        try:
            f=open(filename,'r')
        except FileNotFoundError:
            print('*** 没有"%s"文件，终止任务 ***'%filename)
            sys.exit(1)
        else:
            fbuild_obj=self.read_json(f.read())
        try:
            output=[]
            output.append(fbuild_obj["PkgName"])
            output.append(fbuild_obj["PkgVersion"])
            output.append(fbuild_obj["PkgRelease"])
            output.append(fbuild_obj["PkgBranch"])
            output.append(fbuild_obj["Maintainer"])
            output.append(fbuild_obj["License"])
            output.append(fbuild_obj["Architecture"])
            output.append(fbuild_obj["Dependencies"])
            output.append(fbuild_obj["Target"])
        except KeyError:
            print('*** FBUILD的字段出现了问题，终止任务 ***')
            sys.exit(2)
        return output
    def build(self,filename):
        print("===> 在PATH中检查C/C++编译器")
        PATH=os.environ.get("PATH").split(":")
        CC=None
        GCC_EXIST=False
        CLANG_EXIST=False
        for x in PATH:
            if os.path.isfile("%s/gcc"%x):
                GCC_EXIST=True
            if os.path.isfile("%s/clang"%x):
                CLANG_EXIST=True
        if GCC_EXIST and CLANG_EXIST:
            while not CC:
                i=input("请选择需要使用的编译器(1:gcc,2:clang)>")
                if i=='1':
                    CC='gcc'
                if i=='2':
                    CC='clang'
                else:
                    print("*** 您必须选择一个编译器 ***") 
        else:
            print("*** 没有编译器，终止任务 ***")
            
    def read_json(self,json_str):
        try:
            return json.loads(json_str)
        except json.decoder.JSONDecodeError:
            print('*** FBUILD中JSON语法出现错误，终止任务 ***')
            sys.exit(2)
