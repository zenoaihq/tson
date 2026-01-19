import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { promises as fs } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import {
    prettify,
    minify,
    loadJson,
    loadTson,
    saveTson,
    saveTsonString,
    jsonToTson,
    tsonToJson,
    readTsonString,
    prettifyFile,
    minifyFile,
    dumps,
    loads,
} from '../src/index';

describe('Prettify and Minify', () => {
    it('should prettify simple tabular TSON', () => {
        const input = '{@id,name#2|1,Alice|2,Bob}';
        const pretty = prettify(input);
        expect(pretty).toContain('\n');
        expect(pretty).toContain('|1,Alice');
        expect(pretty).toContain('|2,Bob');
    });

    it('should prettify single object TSON', () => {
        const input = '{@name,age|Alice,30}';
        const pretty = prettify(input);
        expect(pretty).toContain('\n');
        expect(pretty).toContain('|Alice,30');
    });

    it('should prettify arrays', () => {
        const input = '[1,2,3,4,5]';
        const pretty = prettify(input);
        expect(pretty).toContain('\n');
        expect(pretty.startsWith('[')).toBe(true);
        expect(pretty.endsWith(']')).toBe(true);
    });

    it('should handle empty strings', () => {
        expect(prettify('')).toBe('');
        expect(prettify(null as unknown as string)).toBe(null);
    });

    it('should minify prettified TSON', () => {
        const original = '{@id,name#2|1,Alice|2,Bob}';
        const pretty = prettify(original);
        const minified = minify(pretty);
        expect(minified).toBe(original);
    });

    it('should minify multi-line TSON', () => {
        const input = `{@id,name#2
    |1,Alice
    |2,Bob}`;
        const minified = minify(input);
        expect(minified).toBe('{@id,name#2|1,Alice|2,Bob}');
    });

    it('should handle nested structures', () => {
        const input = '{@name,items|Alice,[1,2,3]}';
        const pretty = prettify(input);
        const minified = minify(pretty);
        expect(minified).toBe(input);
    });
});

describe('File I/O', () => {
    let testDir: string;

    beforeAll(async () => {
        testDir = join(tmpdir(), 'tson-test-' + Date.now());
        await fs.mkdir(testDir, { recursive: true });
    });

    afterAll(async () => {
        try {
            await fs.rm(testDir, { recursive: true });
        } catch {
            // Ignore cleanup errors
        }
    });

    it('should load and save JSON files', async () => {
        const testData = { name: 'Alice', age: 30 };
        const jsonPath = join(testDir, 'test.json');

        await fs.writeFile(jsonPath, JSON.stringify(testData));
        const loaded = await loadJson(jsonPath);
        expect(loaded).toEqual(testData);
    });

    it('should save and load TSON files', async () => {
        const testData = [
            { id: 1, name: 'Alice' },
            { id: 2, name: 'Bob' },
        ];
        const tsonPath = join(testDir, 'test.tson');

        await saveTson(testData, tsonPath);
        const loaded = await loadTson(tsonPath);
        expect(loaded).toEqual(testData);
    });

    it('should save pretty-formatted TSON', async () => {
        const testData = [
            { id: 1, name: 'Alice' },
            { id: 2, name: 'Bob' },
        ];
        const tsonPath = join(testDir, 'pretty.tson');

        await saveTson(testData, tsonPath, { format: 'pretty' });
        const content = await fs.readFile(tsonPath, 'utf-8');
        expect(content).toContain('\n');
    });

    it('should save TSON string directly', async () => {
        const tsonStr = '{@id,name#2|1,Alice|2,Bob}';
        const tsonPath = join(testDir, 'direct.tson');

        await saveTsonString(tsonStr, tsonPath);
        const loaded = await readTsonString(tsonPath);
        expect(loaded).toBe(tsonStr);
    });

    it('should convert JSON to TSON', async () => {
        const testData = [
            { id: 1, name: 'Alice' },
            { id: 2, name: 'Bob' },
        ];
        const jsonPath = join(testDir, 'convert.json');
        const tsonPath = join(testDir, 'convert.tson');

        await fs.writeFile(jsonPath, JSON.stringify(testData));
        const tsonStr = await jsonToTson(jsonPath, tsonPath);

        expect(tsonStr).toBeTruthy();
        const loaded = await loadTson(tsonPath);
        expect(loaded).toEqual(testData);
    });

    it('should convert TSON to JSON', async () => {
        const testData = [
            { id: 1, name: 'Alice' },
            { id: 2, name: 'Bob' },
        ];
        const tsonPath = join(testDir, 'convert2.tson');
        const jsonPath = join(testDir, 'convert2.json');

        await saveTson(testData, tsonPath);
        const jsonStr = await tsonToJson(tsonPath, jsonPath);

        expect(jsonStr).toBeTruthy();
        const loaded = await loadJson(jsonPath);
        expect(loaded).toEqual(testData);
    });

    it('should prettify file in place', async () => {
        const tsonStr = '{@id,name#2|1,Alice|2,Bob}';
        const tsonPath = join(testDir, 'prettify.tson');

        await saveTsonString(tsonStr, tsonPath);
        await prettifyFile(tsonPath);
        const content = await fs.readFile(tsonPath, 'utf-8');
        expect(content).toContain('\n');
    });

    it('should minify file in place', async () => {
        const prettyTson = `{@id,name#2
    |1,Alice
    |2,Bob}`;
        const tsonPath = join(testDir, 'minify.tson');

        await saveTsonString(prettyTson, tsonPath);
        await minifyFile(tsonPath);
        const content = await fs.readFile(tsonPath, 'utf-8');
        expect(content).toBe('{@id,name#2|1,Alice|2,Bob}');
    });
});

describe('Round-trip with new functions', () => {
    it('should preserve data through prettify/minify cycle', () => {
        const data = [
            { id: 1, name: 'Alice', tags: ['a', 'b'] },
            { id: 2, name: 'Bob', tags: ['c', 'd'] },
        ];

        const tson = dumps(data);
        const pretty = prettify(tson);
        const minified = minify(pretty);
        const parsed = loads(minified);

        expect(parsed).toEqual(data);
    });

    it('should preserve nested arrays through prettify/minify', () => {
        const data = [
            { name: 'Alice', items: [{ x: 1 }, { x: 2 }] },
            { name: 'Bob', items: [{ x: 3 }, { x: 4 }] },
        ];

        const tson = dumps(data);
        const pretty = prettify(tson);
        const minified = minify(pretty);
        const parsed = loads(minified);

        expect(parsed).toEqual(data);
    });
});
