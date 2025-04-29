// ModelWorker.js
import * as THREE from 'three'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js'
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader.js'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js'

self.onmessage = async function(e) {
  const { filePath } = e.data
  const ext = filePath.split('.').pop().toLowerCase()
  let loader

  if (ext === 'obj') {
    loader = new OBJLoader()
  } else if (ext === 'ply') {
    loader = new PLYLoader()
  } else if (ext === 'stl') {
    loader = new STLLoader()
  } else {
    self.postMessage({ error: 'Unsupported file format: ' + ext })
    return
  }

  try {
    const object = await new Promise((resolve, reject) => {
      loader.load(
        filePath,
        resolve,
        undefined,
        reject
      )
    })

    let mesh
    if (ext === 'ply' || ext === 'stl') {
      mesh = new THREE.Mesh(object, new THREE.MeshStandardMaterial({ color: 0xcccccc, side: THREE.DoubleSide }))
    } else {
      mesh = object
    }

    const json = mesh.toJSON()
    self.postMessage({ json })
  } catch (error) {
    self.postMessage({ error: error.message })
  }
}
