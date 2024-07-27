<script>
	// Receive x-scale, height and margins as props.
	export let xScale;
	export let height;
	export let margin;

	// Determine ticks based on x-scale.
	// Try changing this number to haver e.g. fewer ticks.
	$: xTicks = xScale.ticks(10);

	// Prepare a formatting function to wrangle the dates into "just years"
	import { timeFormat } from 'd3-time-format';
	const timeFormatter = timeFormat('%Y');
</script>

<g class="x-axis" transform="translate(0, {height - margin.bottom})">
	<!-- 
		Loop through the x-ticks defined in the script tag 
		and define a tick with it's label respectively.
	-->
	{#each xTicks as tick, index}
		<g class="tick" transform="translate({xScale(tick)}, 0)">
			<!-- X-Axis Ticks -->
			<line x1={0} x2={0} y1={0} y2={6} stroke="hsla(212, 10%, 53%, 1)" />

			<!-- X-Axis Tick Labels -->
			<text y={6} dy={9} fill="currentColor" text-anchor="middle" dominant-baseline="middle">
				{tick}
			</text>
		</g>
	{/each}
</g>
