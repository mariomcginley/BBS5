###
# Bulbflow code
###
from bulbs.rexster import Graph, Config, REXSTER_URI
from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, Long, Float, List, Dictionary, DateTime
from bulbs.utils import current_datetime
from bulbs.config import DEBUG

import hashlib

config = Config("http://localhost:8182/graphs/bbs", "root", "root")
g = Graph(config)
g.scripts.update('gremlin.groovy')
g.config.set_logger(DEBUG)

class Account(Node):
    element_type = "account"

    screen_name = String(nullable=False)
    password = String(nullable=False)
    email = String(nullable=False)
    first_name = String(nullable=False)
    last_name = String(nullable=False)

class RootFolderContainer(Node):
    element_type = "root_folder_container"

class ContentRoot(Relationship):
    label = "content_root"

class Knows(Relationship):
    label = "knows"

class Principal(Relationship):
    label = "principal"

class IsMemberOfGroup(Relationship):
    label = "is_member_of_group"

class Group(Node):
    element_type = "group"

    name = String(nullable=False)

class Security(Relationship):
    label = "security"

    flags = String()

class HasChildContent(Relationship):
    label = "has_child_content"


class Object(Node):
    element_type = "obj"

    name = String(nullable=False)
    type = String(nullable=False)

class ObjToProperty(Relationship):
    label = "obj_to_property"

class StringProperty(Node):
    element_type = "str_prop"

    is_property = Integer(default=1)
    name = String()
    value = String()

class IntegerProperty(Node):
    element_type = "int_prop"

    is_property = Integer(default=1)
    name = String()
    value = Integer()

class LongProperty(Node):
    element_type = "long_prop"

    is_property = Integer(default=1)
    name = String()
    value = Long()

class FloatProperty(Node):
    element_type = "float_prop"

    is_property = Integer(default=1)
    name = String()
    value = Float()

class ListProperty(Node):
    element_type = "list_prop"

    is_property = Integer(default=1)
    name = String()
    value = List()

class DictionaryProperty(Node):
    element_type = "dict_prop"

    is_property = Integer(default=1)
    name = String()
    value = Dictionary()

class DateTimeProperty(Node):
    element_type = "datetime_prop"

    is_property = Integer(default=1)
    name = String()
    value = DateTime()

g.add_proxy("accounts", Account)
g.add_proxy("principals", Principal)
g.add_proxy("objs", Object)
g.add_proxy("root_folder_container", RootFolderContainer)
g.add_proxy("str_prop", StringProperty)
g.add_proxy("int_prop", IntegerProperty)
g.add_proxy("long_prop", LongProperty)
g.add_proxy("float_prop", FloatProperty)
g.add_proxy("list_prop", ListProperty)
g.add_proxy("dict_prop", DictionaryProperty)
g.add_proxy("datetime_prop", DateTimeProperty)

g.add_proxy("content_root", ContentRoot)
g.add_proxy("obj_to_properties", ObjToProperty)
g.add_proxy("principal", Principal)
g.add_proxy("is_member_of_group", IsMemberOfGroup)
g.add_proxy("groups", Group)
g.add_proxy("security", Security)
g.add_proxy("has_child_content", HasChildContent)
g.add_proxy("knows", Know)

class ACL(object):
    def create_account(screen_name, password, email, first_name, last_name):
        account = g.accounts.create(screen_name, hashlib.sha224(password), email, first_name, last_name)

        # link account to "All Principals" group
        all_principals = yield from g.gremlin.nb_query(db.g.scripts.get('get_group'),{'group': 'All Principals'})
        all_principals = yield from all_principals.__next__()
        g.is_member_of_group.create(account, all_principals)

        # create Home folder for account
        home_folder = yield from g.gremlin.nb_query(db.g.scripts.get('get_by_path'),{'path': '/Home'})
        home_folder = yield from home_folder.__next__()
        user_home = g.objs.create(type='Folder', name=screen_name)
        g.has_child_content.create(home_folder, user_home)
        public = g.objs.create(type='Folder', name='Public')
        private = g.objs.create(type='Folder', name='Private')
        g.has_child_content.create(user_home, public)
        g.has_child_content.create(user_home, private)
        g.security.create(all_principals, public, flags="r")
        g.security.create(account, private)

    def has_read_access(account, path):
        obj = yield from g.gremlin.nb_query(db.g.scripts.get('get_by_path'),{'path': path})
        obj = yield from obj.__next__()



acl = ACL()




###
# Redis code
###
import redis

config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config)





def bootstrap():
    vertices = g.V
    try:
        for vertex in vertices:
            g.vertices.delete(vertex.eid)
        #edges = g.E
        #for edge in edges:
        #    g.edges.delete(edge.eid)
    except:
        print('failed to reset db')


    root_folder_container = g.root_folder_container.create()
    root_folder = g.objs.create(name='Root Folder', type='Folder')
    g.content_root.create(root_folder_container, root_folder)
    home_folder = g.objs.create(name='Home', type='Folder')
    g.has_child_content(root_folder, home_folder)

    admin = acl.create_account(screen_name='admin', password='test', email="mario.cristo.mcginley@gmail.com", first_name="Mario", last_name="McGinley")
    mario = acl.create_account(screen_name="artreth", password='test', email="mario.cristo.mcginley@gmail.com", first_name="Mario", last_name="McGinley")
    g.knows.create(admin, mario)
    g.knows.create(mario, admin)

    all_principals = g.groups.create(name='Everybody')
    regular_users = g.groups.create(name='Regular Users')
    super_users = g.groups.create(name='Super Users')
    g.is_member_of_group(regular_users, all_principals)
    g.is_member_of_group(super_users, all_principals)

    g.security.create(all_principals, root_folder, flags="r")
