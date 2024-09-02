import os 
class PathNode:
    def __init__(self) -> None:
        self.dir_name = ""
        self.path_tag = False
        self.sub_dir = {}

class PathShortener:
    def __init__(self, paths) -> None:
        self.paths = paths
        self.root = PathNode()
        self.root.dir_name = "Root"
        for path in self.paths:
            self.addPath(path)
    
    def addPath(self, path):
        path_list = []
        # print(path)
        while True:
            path_list = [os.path.basename(path)] +path_list 
            path = os.path.dirname(path)
            if path == os.path.dirname(path):
                path_list = [path] +path_list 
                break
        temp = self.root
        path_list[0] = path_list[0].rstrip("\\")
        for i in range(len(path_list)):
            dr_name = path_list[i]
            try:
                temp = temp.sub_dir[dr_name]
                if i == 0 or i == len(path_list)-2 or i == len(path_list)-1:
                    temp.path_tag = True
            except:
                temp.sub_dir[dr_name] = PathNode()
                temp = temp.sub_dir[dr_name]
                temp.dir_name = dr_name
                if i == 0 or i == len(path_list)-2 or i == len(path_list)-1:
                    temp.path_tag = True
    def getPaths(self):
        self.res = []
        def f(node, cur_path):
            if node.path_tag:
                cur_path += f">>{node.dir_name}"
            for c_node in node.sub_dir.values():
                f(c_node, cur_path)
            if not node.sub_dir.values():
                # self.res.append(cur_path[2:])
                if cur_path:
                    self.res.append(cur_path[2:4] + ">>..."+ cur_path[4:])
        f(self.root, "")
        return self.res

def path_shorten(paths):
    PS = PathShortener(paths=paths)
    return PS.getPaths()
