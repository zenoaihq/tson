/**
 * TSON File Utilities
 *
 * Convenience functions for working with TSON and JSON files.
 * Includes support for:
 * - Loading JSON/TSON files
 * - Saving to TSON with formatting options
 *
 * Note: These functions are Node.js only (use dynamic imports for fs).
 */

import { dumps } from './serializer';
import { loads } from './deserializer';
import { prettify, minify } from './prettify';

type FormatOption = 'compact' | 'pretty';

/**
 * Load a JSON file and return JavaScript data structure.
 *
 * @example
 * const data = await loadJson('data.json');
 *
 * @param filepath - Path to JSON file
 * @returns Parsed JavaScript object
 */
export async function loadJson(filepath: string): Promise<unknown> {
    const fs = await import('fs/promises');
    const content = await fs.readFile(filepath, 'utf-8');
    return JSON.parse(content);
}

/**
 * Load a TSON file and return JavaScript data structure.
 *
 * @example
 * const data = await loadTson('data.tson');
 *
 * @param filepath - Path to TSON file
 * @returns Parsed JavaScript object
 */
export async function loadTson(filepath: string): Promise<unknown> {
    const fs = await import('fs/promises');
    const content = await fs.readFile(filepath, 'utf-8');
    return loads(content);
}

/**
 * Save JavaScript data to a TSON file.
 *
 * @example
 * await saveTson(data, 'output.tson');
 * await saveTson(data, 'output.tson', { format: 'pretty' });
 *
 * @param data - JavaScript object to serialize
 * @param filepath - Output file path
 * @param options - Formatting options
 */
export async function saveTson(
    data: unknown,
    filepath: string,
    options: { format?: FormatOption; indent?: string } = {}
): Promise<void> {
    const fs = await import('fs/promises');

    // Serialize to TSON
    let tsonStr = dumps(data as import('./types').TSONValue);

    // Apply formatting
    if (options.format === 'pretty') {
        tsonStr = prettify(tsonStr, options.indent || '  ');
    }

    await fs.writeFile(filepath, tsonStr, 'utf-8');
}

/**
 * Save a TSON string directly to file.
 *
 * @example
 * await saveTsonString(tsonData, 'output.tson');
 * await saveTsonString(tsonData, 'output.tson', { format: 'pretty' });
 *
 * @param tsonStr - TSON formatted string
 * @param filepath - Output file path
 * @param options - Formatting options
 */
export async function saveTsonString(
    tsonStr: string,
    filepath: string,
    options: { format?: FormatOption | null; indent?: string } = {}
): Promise<void> {
    const fs = await import('fs/promises');

    // Apply formatting if requested
    if (options.format === 'pretty') {
        tsonStr = prettify(tsonStr, options.indent || '  ');
    } else if (options.format === 'compact') {
        tsonStr = minify(tsonStr);
    }

    await fs.writeFile(filepath, tsonStr, 'utf-8');
}

/**
 * Convert a JSON file to TSON format.
 *
 * @example
 * const tsonStr = await jsonToTson('data.json');
 * await jsonToTson('data.json', 'data.tson');
 *
 * @param inputPath - Path to input JSON file
 * @param outputPath - Path to output TSON file (optional)
 * @param options - Formatting options
 * @returns TSON string representation
 */
export async function jsonToTson(
    inputPath: string,
    outputPath?: string,
    options: { format?: FormatOption } = {}
): Promise<string> {
    const data = await loadJson(inputPath);
    let tsonStr = dumps(data as import('./types').TSONValue);

    if (options.format === 'pretty') {
        tsonStr = prettify(tsonStr);
    }

    if (outputPath) {
        await saveTsonString(tsonStr, outputPath);
    }

    return tsonStr;
}

/**
 * Convert a TSON file to JSON format.
 *
 * @example
 * const jsonStr = await tsonToJson('data.tson');
 * await tsonToJson('data.tson', 'data.json');
 *
 * @param inputPath - Path to input TSON file
 * @param outputPath - Path to output JSON file (optional)
 * @param options - Formatting options
 * @returns JSON string representation
 */
export async function tsonToJson(
    inputPath: string,
    outputPath?: string,
    options: { indent?: number } = {}
): Promise<string> {
    const data = await loadTson(inputPath);
    const jsonStr = JSON.stringify(data, null, options.indent ?? 2);

    if (outputPath) {
        const fs = await import('fs/promises');
        await fs.writeFile(outputPath, jsonStr, 'utf-8');
    }

    return jsonStr;
}

/**
 * Read a TSON file as raw string (without parsing).
 *
 * Useful when you want to prettify/minify without deserializing.
 *
 * @param filepath - Path to TSON file
 * @returns Raw TSON string
 */
export async function readTsonString(filepath: string): Promise<string> {
    const fs = await import('fs/promises');
    return fs.readFile(filepath, 'utf-8');
}

/**
 * Prettify a TSON file in place or to a new file.
 *
 * @param inputPath - Path to input TSON file
 * @param outputPath - Path to output file (default: overwrite input)
 * @param indent - Indentation string (default: 2 spaces)
 * @returns Prettified TSON string
 */
export async function prettifyFile(
    inputPath: string,
    outputPath?: string,
    indent: string = '  '
): Promise<string> {
    const tsonStr = await readTsonString(inputPath);
    const prettyStr = prettify(tsonStr, indent);

    const target = outputPath || inputPath;
    await saveTsonString(prettyStr, target);

    return prettyStr;
}

/**
 * Minify a TSON file in place or to a new file.
 *
 * @param inputPath - Path to input TSON file
 * @param outputPath - Path to output file (default: overwrite input)
 * @returns Minified TSON string
 */
export async function minifyFile(
    inputPath: string,
    outputPath?: string
): Promise<string> {
    const tsonStr = await readTsonString(inputPath);
    const compactStr = minify(tsonStr);

    const target = outputPath || inputPath;
    await saveTsonString(compactStr, target);

    return compactStr;
}
