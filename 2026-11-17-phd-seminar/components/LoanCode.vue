<script setup lang="ts">
// Sources of the loan example: both versions of approvedAmount, the developer test of the
// full approval and the generalized test that Teralizer derives from it.
//   v2:      the whole method after the cleanup
//   v2body, v1body: the method bodies with the line numbers of the whole methods, which
//            share their signature
//   test, property: the property is the generated jqwik test in the notation of the thesis
//            (Listing lst:pricing-property). The generated supplier bounds amount at 60
//            and filters on the path condition. The recorded condition reads p > 0.8, and
//            the slide writes >= as the code does. Its parameters are i, d and a for income,
//            debt and amount, so that the assertion fits on one line, and comments give
//            the full names. `p(i, d)` stands for the formula of p over income and debt
//            (lines 6 and 7 of the method), so that the condition reads as on the map.
const props = withDefaults(defineProps<{
  name: 'v2' | 'v2body' | 'v1body' | 'test' | 'property'
  marked?: boolean
  focus?: number[]
}>(), { marked: true, focus: () => [] })

const v2body = `  final int FULL = 50;
  final int PARTIAL = 5;

  double risk = (3.0 * debt - income) / 100.0;
  double p = 1 / (1 + Math.exp(risk));

  if (p >= 0.8) return Math.min(amount, FULL);
  if (p >= 0.5) return Math.min(amount, PARTIAL);
  return 0;`
const signature = `int approvedAmount(
    int income, int debt, int amount) {`
const v2keys = { 9: 'full', 10: 'partial', 11: 'reject' }

const sources = {
  v2: { code: `${signature}\n${v2body}\n}`, marks: ['3:50'], keys: v2keys },
  v2body: { code: v2body, marks: ['3:50'], keys: v2keys, numbers: [3, 4, 5, 6, 7, 8, 9, 10, 11] },
  v1body: {
    code: `  double risk = (3.0 * debt - income) / 100.0;
  double p = 1 / (1 + Math.exp(risk));

  if (p < 0.5) return 0;
  return Math.min(amount, p >= 0.8 ? 60 : 5);`,
    marks: ['7:60'],
    numbers: [3, 4, 5, 6, 7],
  },
  test: {
    code: `@Test
void fullApproval() {
  assertEquals(20, approvedAmount(300, 10, 20));
}`,
  },
  property: {
    code: `@Property
void fullApproval(
    @ForAll int i, // income
    @ForAll int d, // debt
    @ForAll @IntRange(max = 60) int a // amount
) {
  Assume.that(p(i, d) >= 0.8);
  assertEquals(a, approvedAmount(i, d, a));
}`,
    tints: { 5: 'in', 7: 'in', 8: 'out' },
  },
}
</script>

<template>
  <JavaCode v-bind="sources[props.name]" :marked="marked" :focus="focus" />
</template>
