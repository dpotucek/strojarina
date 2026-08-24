function parseFlexibleNumber(value) {
    const text = String(value).trim().replace(',', '.').replace('⁄', '/');
    if (!text) return NaN;

    const mixed = text.match(/^([+-]?(?:\d+(?:\.\d*)?|\.\d+))(?:\s+|-)(\d+)\/(\d+)$/);
    if (mixed) {
        const denominator = Number(mixed[3]);
        if (denominator === 0) return NaN;
        return Number(mixed[1]) + Number(mixed[2]) / denominator;
    }

    const fraction = text.match(/^([+-]?\d+)\/(\d+)$/);
    if (fraction) {
        const denominator = Number(fraction[2]);
        return denominator === 0 ? NaN : Number(fraction[1]) / denominator;
    }

    return Number(text);
}
