from colorama import Fore, Back, Style

def factorielle(n):
    if n == 1:
        return 1
    result = n * factorielle (n-1)
    print(f"{n}! = {result}")
    return result

def nombre_messages(obj):
    '''
    Cette fonction doit retourner le nombre de messages contenus dans l'obj
    :param  obj: objet JSON
    :return: Nombre de messages trouvés
    '''
    cumul = 1
    print(f"id:{obj['id']} - depth {obj['depth'] if 'depth' in obj else '-'}, count {obj['comments_count'] if 'comments_count' in obj else '-'}, ")
    # depth = obj['depth'] if 'depth' in obj else -1
    # print(f"{'  ' * (depth+1)}id: {Fore.RED}{obj['id']}{Style.RESET_ALL}, depth: {depth}, count: {obj['comments_count'] if 'comments_count' in obj else '-'}")
    if 'children' in obj:
        for msg in obj['children']:
            cumul += nombre_messages(msg)
    if XXXXXXXXXXXXXXX
    print(f"id: {obj['id']}  = {cumul} messages")
    return cumul