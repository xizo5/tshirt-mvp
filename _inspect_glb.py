import json, struct, sys

def inspect(path):
    with open(path, "rb") as f:
        magic, ver, length = struct.unpack("<III", f.read(12))
        chunk_len, chunk_type = struct.unpack("<II", f.read(8))
        gltf = json.loads(f.read(chunk_len).decode("utf-8"))
        bin_chunk_len, _ = struct.unpack("<II", f.read(8))
        bin_data = f.read(bin_chunk_len)
    print("===", path)
    print("meshes:", len(gltf.get("meshes", [])))
    print("materials:", [m.get("name") for m in gltf.get("materials", [])])
    # compute bbox from POSITION accessors
    mins = [1e9,1e9,1e9]; maxs = [-1e9,-1e9,-1e9]
    has_uv = False
    for mesh in gltf.get("meshes", []):
        for prim in mesh["primitives"]:
            pos_acc = gltf["accessors"][prim["attributes"]["POSITION"]]
            mn = pos_acc.get("min"); mx = pos_acc.get("max")
            if mn:
                for i in range(3):
                    mins[i] = min(mins[i], mn[i]); maxs[i] = max(maxs[i], mx[i])
            if "TEXCOORD_0" in prim["attributes"]:
                has_uv = True
    print("bbox min:", [round(x,3) for x in mins])
    print("bbox max:", [round(x,3) for x in maxs])
    print("has UV:", has_uv)
    print("nodes:", [n.get("name") for n in gltf.get("nodes", [])][:10])

for p in sys.argv[1:]:
    inspect(p)
