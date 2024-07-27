<script>
	// Receive y-scale, width and margins as props.
	export let yScale;
	export let width;
	export let margin;

	// Determine ticks based on y-scale.
	// Try changing this number to haver e.g. fewer ticks.
	$: yTicks = yScale.ticks(8);
</script>

<g class="y-axis" transform="translate({margin.left}, 0)">
	<!-- Y-Axis Label -->
	<!-- <text y={9} x={-margin.left} fill="currentColor" dominant-baseline="middle" text-anchor="start">
		↑ Daily close ($)
	</text> -->

	<!-- 
		Loop through the y-ticks defined in the script tag 
		and define a tick with it's label respectively.
	-->
	{#each yTicks as tick, index}
		<g class="tick" transform="translate(0, {yScale(tick)})">
			<!-- Y-Axis Ticks -->
			<line x1={0} x2={width} y1={0} y2={0} stroke="hsla(212, 10%, 53%, 0.3)" />

			<!-- Y-Axis Tick Labels -->
			<text x={-5} y={0} fill="currentColor" dominant-baseline="middle" text-anchor="end">
				{tick}
			</text>
		</g>
	{/each}
</g>
