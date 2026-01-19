/**
 * TSON Prettify
 *
 * Format TSON strings for human readability.
 * CSV-like format: schema on top, one row/value per line.
 */

/**
 * Format a compact TSON string for human readability.
 *
 * Uses CSV-like formatting:
 * - Schema declaration on first line
 * - Each row/value on its own line with leading delimiter
 *
 * @example
 * prettify('{@id,name#2|1,Alice|2,Bob}')
 * // Returns: '{@id,name#2\n|1,Alice\n|2,Bob}'
 *
 * @param tsonStr - Compact TSON string
 * @param indent - Indentation string (default: 2 spaces)
 * @returns Pretty-formatted TSON string
 */
export function prettify(tsonStr: string, indent: string = '  '): string {
    if (!tsonStr || !tsonStr.trim()) {
        return tsonStr;
    }

    return prettifyValue(tsonStr.trim(), indent, 0);
}

/**
 * Remove all formatting from a TSON string.
 *
 * @param tsonStr - Pretty-formatted TSON string
 * @returns Compact single-line TSON string
 */
export function minify(tsonStr: string): string {
    if (!tsonStr) {
        return tsonStr;
    }

    const lines = tsonStr.split('\n');
    const result: string[] = [];

    for (const line of lines) {
        // Remove leading/trailing whitespace but preserve content
        result.push(line.trim());
    }

    return result.join('');
}

/**
 * Recursively prettify a TSON value.
 */
function prettifyValue(text: string, indent: string, depth: number): string {
    text = text.trim();

    if (!text) {
        return text;
    }

    // Object with schema: {@...}
    if (text.startsWith('{@')) {
        return prettifyObject(text, indent, depth);
    }

    // Schematized object (no @): {...}
    if (text.startsWith('{')) {
        return text; // Keep schematized values compact
    }

    // Array: [...]
    if (text.startsWith('[')) {
        return prettifyArray(text, indent, depth);
    }

    // Primitive value
    return text;
}

/**
 * Prettify a TSON object.
 *
 * Format:
 *   {@key1,key2,key3#N
 *   |value1,value2,value3
 *   |value4,value5,value6}
 */
function prettifyObject(text: string, indent: string, depth: number): string {
    if (!text.startsWith('{@') || !text.endsWith('}')) {
        return text;
    }

    // Extract content between {@ and }
    const content = text.slice(2, -1);

    if (!content) {
        return '{@}';
    }

    // Split by | to get schema and values
    const parts = splitTopLevel(content, '|');

    if (parts.length === 0) {
        return text;
    }

    const schema = parts[0];
    const valueRows = parts.slice(1);

    // Build pretty output
    const nextIndent = indent.repeat(depth + 1);

    if (valueRows.length === 0) {
        // Schema only, no values
        return `{@${schema}}`;
    }

    const lines: string[] = [`{@${schema}`];

    for (const row of valueRows) {
        lines.push(`${nextIndent}|${row}`);
    }

    // Close brace on same line as last value
    lines[lines.length - 1] = lines[lines.length - 1] + '}';

    return lines.join('\n');
}

/**
 * Prettify a TSON array.
 *
 * Format:
 *   [value1
 *   ,value2
 *   ,value3]
 */
function prettifyArray(text: string, indent: string, depth: number): string {
    if (!text.startsWith('[') || !text.endsWith(']')) {
        return text;
    }

    const content = text.slice(1, -1);

    if (!content) {
        return '[]';
    }

    // Split array elements
    const elements = splitTopLevel(content, ',');

    if (elements.length <= 1) {
        // Single element or empty, keep compact
        return text;
    }

    const nextIndent = indent.repeat(depth + 1);

    const lines: string[] = [];
    for (let i = 0; i < elements.length; i++) {
        const prettified = prettifyValue(elements[i].trim(), indent, depth + 1);
        if (i === 0) {
            lines.push(`[${prettified}`);
        } else {
            lines.push(`${nextIndent},${prettified}`);
        }
    }

    lines[lines.length - 1] = lines[lines.length - 1] + ']';

    return lines.join('\n');
}

/**
 * Split text by delimiter, respecting nested brackets and quotes.
 */
function splitTopLevel(text: string, delimiter: string): string[] {
    const parts: string[] = [];
    const current: string[] = [];
    let depth = 0;
    let inString = false;
    let escapeNext = false;

    for (let i = 0; i < text.length; i++) {
        const char = text[i];

        if (escapeNext) {
            current.push(char);
            escapeNext = false;
            continue;
        }

        if (char === '\\') {
            current.push(char);
            escapeNext = true;
            continue;
        }

        if (char === '"') {
            inString = !inString;
            current.push(char);
            continue;
        }

        if (inString) {
            current.push(char);
            continue;
        }

        if (char === '{' || char === '[') {
            depth++;
            current.push(char);
        } else if (char === '}' || char === ']') {
            depth--;
            current.push(char);
        } else if (char === delimiter && depth === 0) {
            parts.push(current.join(''));
            current.length = 0;
        } else {
            current.push(char);
        }
    }

    if (current.length > 0) {
        parts.push(current.join(''));
    }

    return parts;
}
