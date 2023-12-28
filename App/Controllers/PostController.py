from App.Model.PostModel import *
class PostControllers:
    def __init__(self):
        self.PostModel = PostModel()
    def AddPost(self, post: Post):
        return self.PostModel.AddPost(post)
    def GetAllPost(self):
        return self.PostModel.GetAllPost()
    def GetAllContentPost(self):
        return self.PostModel.GetAllContentPost()
    def GetAllIDPost(self):
        return self.PostModel.GetAllIDPost()
    def DeleteDuplicatePost(self):
        return self.PostModel.DeleteDuplicatePost()
    def DeleteOldPost(self):
        return self.PostModel.DeleteOldPost()
    def DeletePostByIDPost(self, IDPost: str):
        return self.PostModel.DeletePostByIDPost(IDPost)