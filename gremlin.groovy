def get_group(group) {
    return g.V('element_type', 'group').has('name', group).vertices()
}

def is_allowed(screen_name, obj) {
    user = g.V('element_type', 'account').has('screen_name', screen_name).vertices()[0]
    // check for direct relationship to object
    can_access = 0
    if ( user.both('security').retain([obj]).hasNext() ) {
        can_access = 1
    }
    // check for group relationship to object
    if ( !can_access ) {
        user_belongs_to = user.out('is_member_of_group').vertices()
        for ( group in user_belongs_to ) {
            if ( group.both('security').retain([obj]).hasNext() ) {
                can_access = 1
                break
            }
        }
    }
    if ( can_access ) {
        return True
    }
    else {
        return False
    }    
}

def get_account_by_email(email) {
    return g.query().has('email',EQUAL,email).vertices()
}

def get_account_by_screen_name(screen_name) {
    return g.query().has('screen_name', screen_name).vertices()
}

def get_room_by_keyword(keyword) {
    return g.query().has('element_type', 'room').has('keywords', keyword).vertices()
}

def get_item_properties(id) {
    return g.v(id).out().has('is_property',1).vertices()
}

def get_items_in_room(id) {
    return g.v(id).out().has('element_type', 'item').vertices()
}
