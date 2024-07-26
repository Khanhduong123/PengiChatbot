<script lang="ts">
	import { getContext } from 'svelte';
	const i18n = getContext('i18n');
</script>

<div class="mb-3 flex justify-between items-center">
	<div class=" text-lg font-semibold self-center">{$i18n.t('Roles')}</div>
</div>
