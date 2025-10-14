
# my_post = [{"title":"Title of post 1", "content":"i love piszza", "id":1},
#            {"title":"Title of post 2", "content":"Beaches Love me", "id":2}]


# def find_post(id): #Returns the matching post
#     for p in my_post:
#         if p["id"] == id:   # int vs int comparison
#             return p

# #You’d use enumerate() when you also need the index of the item—like 
# #when you want to delete it from a list using pop(index):        
# def find_delete_post(id): 
#     for index, post in enumerate(my_post):
#         if post["id"] == id:
#             return my_post.pop(index)