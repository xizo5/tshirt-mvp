# -*- coding: utf-8 -*-
import io, base64, os

base = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp"
glb = open(os.path.join(base, "assets", "nour_tshirt.glb"), "rb").read()
b64 = base64.b64encode(glb).decode("ascii")
print("glb bytes:", len(glb), "b64 len:", len(b64))

p = os.path.join(base, "threejs.html")
t = io.open(p, "r", encoding="utf-8").read()

# 1) import GLTFLoader
old_imp = "import { OrbitControls } from 'three/addons/controls/OrbitControls.js';"
new_imp = old_imp + "\nimport { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';"
assert old_imp in t
t = t.replace(old_imp, new_imp, 1)

# 2) replace procedural block
start_marker = "// ---- T-shirt on dress form (lathe torso + sleeves + collar) ----"
end_marker = "// ---- print decal on chest ----"
i0 = t.index(start_marker)
i1 = t.index(end_marker)

new_block = '''// ---- T-shirt material + real GLB model (CC-BY by Nour / Poly Pizza) ----
const shirtMat = new THREE.MeshStandardMaterial({
  color: 0xffffff, roughness: 0.92, metalness: 0.0,
  bumpMap: fabricBump(), bumpScale: 0.015
});

const GLB_B64 = "''' + b64 + '''";
const GLB_BIN = Uint8Array.from(atob(GLB_B64), c => c.charCodeAt(0));
new GLTFLoader().parse(GLB_BIN.buffer, "", (gltf) => {
  const obj = gltf.scene;
  const box = new THREE.Box3().setFromObject(obj);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  // 模型高约 1.1
  const s = 1.1 / size.y;
  obj.scale.setScalar(s);
  obj.position.x = -center.x * s;
  obj.position.y = -box.min.y * s;
  obj.position.z = -center.z * s;
  obj.traverse(o => {
    if (o.isMesh){ o.material = shirtMat; o.castShadow = true; }
  });
  scene.add(obj);
  // 印花贴到胸前正面（z 最前处）
  const frontZ = (box.max.z - box.min.z) * s / 2;
  printMesh.position.set(0, 0.55, frontZ + 0.01);
  applyPrint();
});

// ground shadow catcher
const ground = new THREE.Mesh(new THREE.PlaneGeometry(8, 8),
  new THREE.ShadowMaterial({ opacity: 0.22 }));
ground.rotation.x = -Math.PI/2;
ground.position.y = -0.02;
ground.receiveShadow = true;
scene.add(ground);

'''

t = t[:i0] + new_block + t[i1:]

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("written; file size:", len(t))
