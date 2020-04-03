


def buildRepresentationName(name, nodeid):
    if nodeid is not None:
        return f"{name} {nodeid}"
    else:
        return f"{name}"



def buildTransformationName(roi, representation, transformer, input_transformation, nodeid):
    if input_transformation is None:
        return f"{transformer.name}_rep-{representation.id}_roi-{roi.id}_node-{nodeid}"
    else:
        return f"{transformer.name}_trans-{input_transformation.id}_rep-{representation.id}_roi-{roi.id}_node-{nodeid}"