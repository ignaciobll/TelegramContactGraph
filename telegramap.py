from graphviz import Graph
import telegram_queries as tdb


dot = Graph('G',engine="circo",format='svg')
users = tdb.get_users_n_names()
groups = tdb.get_groups_n_title()

for user,first_name in users:
    if user == 339459287: first_name = "RUSO"
    if first_name == "": first_name = str(user)
    dot.node(str(user),label=str(first_name))

for group,title in groups:
    dot.node(str(group),label=str(title), style="filled")


# user = 849577
total = len(users)
current = 0
for user,fn in users:
    # print("{}\tof total".format(current,total))
    current += 1
    user_groups = tdb.get_groups_of_user(user)
    for group in user_groups:
        dot.edge(str(user),str(group))

# dot.render('./round-table.gv', view=True)
print(dot.source)
