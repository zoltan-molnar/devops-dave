def get_team_id(lex_user_id):
    # This one works with Slack, no idea about the others

    return ':'.join(str(lex_user_id).split(':')[:2])


def get_user_id(lex_user_id):
    return str(lex_user_id)
