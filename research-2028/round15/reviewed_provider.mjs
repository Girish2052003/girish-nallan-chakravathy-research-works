// FIPS 203 ML-KEM through Node WebCrypto. No protocol-specific arithmetic.
import { webcrypto } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const subtle = webcrypto.subtle;
const widths = new Map([[512, 768], [768, 1088], [1024, 1568]]);

function algorithm(profile) {
  if (!widths.has(profile)) throw new RangeError('Unrecognized ML-KEM profile');
  return 'ML-KEM-' + profile;
}

export async function keygen(profile) {
  const pair = await subtle.generateKey(algorithm(profile), true, ['encapsulateBits', 'decapsulateBits']);
  const pub = await subtle.exportKey('raw-public', pair.publicKey);
  const seed = await subtle.exportKey('raw-seed', pair.privateKey);
  return [Buffer.from(pub), Buffer.from(seed)];
}

export async function publicFromPrivate(profile, seed) {
  const privateKey = await subtle.importKey('raw-seed', seed, algorithm(profile), true, ['decapsulateBits']);
  const publicKey = await subtle.getPublicKey(privateKey, ['encapsulateBits']);
  return Buffer.from(await subtle.exportKey('raw-public', publicKey));
}

export async function encaps(profile, publicBytes) {
  const name = algorithm(profile);
  const key = await subtle.importKey('raw-public', publicBytes, name, false, ['encapsulateBits']);
  const { ciphertext, sharedKey } = await subtle.encapsulateBits(name, key);
  return [Buffer.from(ciphertext), Buffer.from(sharedKey)];
}

export async function decaps(profile, seed, ciphertext) {
  const name = algorithm(profile);
  const key = await subtle.importKey('raw-seed', seed, name, false, ['decapsulateBits']);
  return Buffer.from(await subtle.decapsulateBits(name, key, ciphertext));
}

async function run() {
  const [operation, profileText] = process.argv.slice(2);
  const profile = Number(profileText);
  algorithm(profile);
  const input = readFileSync(0);
  switch (operation) {
    case 'keygen': return Buffer.concat(await keygen(profile));
    case 'public': return publicFromPrivate(profile, input);
    case 'encaps': return Buffer.concat(await encaps(profile, input));
    case 'decaps':
      if (input.length !== 64 + widths.get(profile)) throw new RangeError('Invalid input length');
      return decaps(profile, input.subarray(0, 64), input.subarray(64));
    default: throw new RangeError('Unknown ML-KEM operation');
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(await run());
  } catch (error) {
    // Standard output is reserved for the binary protocol. Preserve provider
    // failure type without printing key material or a supplied byte string.
    process.stderr.write('ML-KEM provider: ' + error.name + '\n');
    process.exitCode = error.name === 'DataError' ? 2 : 1;
  }
}
