def get_team_id(lex_user_id):
    # This one works with Slack, no idea about the others
    partials = str(lex_user_id).split(':')
    return partials[0] + ':' + partials[1]


def get_user_id(lex_user_id):
    return str(lex_user_id)
