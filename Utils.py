def flatToTree(dataSet):
    nodes = {}
    for data in dataSet:
        id = data['id']
        nodes[id] = {'data': data}

    forest = []
    for data in dataSet:
        id = data['id']
        parentId = data['parent_id']
        node = nodes[id]

        if id == parentId:
            forest.append(node)
        else:
            parent = nodes[parentId]
            if not 'children' in parent:
                parent['children'] = []
            children = parent['children']
            children.append(node)

    return forest


def printTree(tree):
    if not 'children' in tree:
        return '<div>{}</div>'.format(tree['data']['id'])
    else:
        text = '<div><title>{}</title>'.format(tree['data']['id'])
        for child in tree['children']:
            text += printTree(child)
        return text + '</div>'
