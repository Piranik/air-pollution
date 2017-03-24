export const TOGGLE_IN_CART = "TOGGLE_IN_CART"
export const ADD_ADDON = "ADD_ADDON"
export const FINALIZE_ORDER = "FINALIZE_ORDER"


export function toggle_in_cart(index) {
	return {
		type: TOGGLE_IN_CART,
    	index: index
	}
}

export function add_addon(addon_index, index) {
	return {
		type: ADD_ADDON,
    	index: index,
    	addon_index: addon_index
	}
}


export function finalize_order() {
	return {
		type: FINALIZE_ORDER
	}
}
