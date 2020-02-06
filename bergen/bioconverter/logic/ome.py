imagetree = {
    "objective": {  "type": "single",
                    "key": "ObjectiveSettings",
                    "values": {
                            "RefractiveIndex": float,
                            "Medium": str
                   }
    },
    "detector": {   "type": "single",
                    "key": "Detector",
                    "values": {
                            "Model": str,
                            "Type": str
                   }
    },
    "scan" : {    "type": "single",
                  "key": "Pixels",
                    "values": {
                            "DimensionOrder": str,
                            "SizeX": int,
                            "SizeY": int,
                            "SizeC": int,
                            "SizeZ": int,
                            "SizeT": int,
                            "PhysicalSizeX": float,
                            "PhysicalSizeY": float,
                            "PhysicalSizeZ": float,
                            "TimeIncrement": float,
                            "PhysicalSizeXUnit": str,
                            "PhysicalSizeYUnit": str,
                            "PhysicalSizeZUnit": str,
                            "SignificantBits": int,
                            "Type": str, #TODO: cast to numpy
                            }
    },
    "channels":  {  "type": "multiple",
                    "key": "Channel",
                    "values": {
                            "Name": str,
                            "EmissionWavelength": float,
                            "ExcitationWavelength": float,
                            "IlluminationType": str,
                            "AcquisitionMode": str,
                            "Color": str,
                            "SamplesPerPixel": int,
                            },
                    },
    "planes": { "type": "multiple",
                "key": "Plane",
                    "values": {
                            "PositionZ": float,
                            "PositionZUnit": str,
                            "TheZ": int,
                            "TheC": int,
                            "TheT": int,
                            "ExposureTime": float,
                            "DeltaT": float,
                            "PositionX": float,
                            "PositionY": float,
    }
                },
}