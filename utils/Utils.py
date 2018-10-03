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


def printTreeToHtml(tree):
    if not 'children' in tree:
        return '<li>{}</li>'.format(tree['data']['id'])
    else:
        text = '<li><bold>children of categoryId {}:</bold></li><ul>'.format(tree['data']['id'])
        for child in tree['children']:
            text += printTreeToHtml(child)
        return text + '</ul>'


def categoryElementToBoolean(element):
    if element is not None:
        return True
    else:
        return False


def printToFile(fileName, input):
    path = 'resources/{}'.format(fileName)
    f = open(path, "w+")
    f.write(input)
    print('results will be found in {}'.format(path))
