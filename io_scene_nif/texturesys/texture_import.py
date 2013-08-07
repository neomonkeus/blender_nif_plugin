"""This script contains helper methods to import textures."""

# ***** BEGIN LICENSE BLOCK *****
# 
# Copyright © 2005-2013, NIF File Format Library and Tools contributors.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#	* Redistributions of source code must retain the above copyright
#	  notice, this list of conditions and the following disclaimer.
# 
#	* Redistributions in binary form must reproduce the above
#	  copyright notice, this list of conditions and the following
#	  disclaimer in the documentation and/or other materials provided
#	  with the distribution.
# 
#	* Neither the name of the NIF File Format Library and Tools
#	  project nor the names of its contributors may be used to endorse
#	  or promote products derived from this software without specific
#	  prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****


import bpy

from pyffi.formats.nif import NifFormat

class Texture():

	def __init__(self, parent):
		self.nif_import = parent
		self.textureloader = None
		self.used_slots = []
		self.b_mat = None
		diffusetextures = []
		bumpmaptextures = []
		normalmaptextures = []
		glowtextures = []
		
		
	def set_texture_loader(self, textureloader):
		self.textureloader = textureloader

	def import_nitextureprop_textures(self, b_mat, n_texture_prop):

		if n_texture_prop.has_base_texture:
			self.import_diffuse_texture(b_mat, n_texture_prop)
	
		if n_texture_prop.has_bump_map_texture:
			self.import_bump_texture(b_mat, n_texture_prop)
				
		if n_texture_prop.has_bump_map_texture:
			self.import_bump_texture(b_mat, n_texture_prop)
			has_normal_texture		
		
		if n_texture_prop.has_glow_texture:
			self.import_glow_texture(b_mat, n_texture_prop)
				
		if n_texture_prop.has_gloss_texture:
			self.import_gloss_texture(b_mat, n_texture_prop)
			
		if n_texture_prop.has_dark_texture:
			self.import_dark_texture(b_mat, n_texture_prop)
		
		if n_texture_prop.has_detail_texture:
			self.import_detail_texture(b_mat, n_texture_prop)
			
# 		has_base_texture
# 	 	has_bump_map_texture
# 	 	has_dark_texture
# 	 	has_decal_0_texture
# 	 	has_decal_1_texture
# 	 	has_decal_2_texture
# 	 	has_decal_3_texture
# 	 	has_detail_texture
# 	 	has_gloss_texture
# 	 	has_glow_texture
# 	 	has_normal_texture
# 	 	has_unknown_2_texture	
			
	def import_texture_extra_shader(b_mat,n_texture_prop, extra_datas):
		# extra texture shader slots
		for shader_tex_desc in n_texture_prop.shader_textures:
			
			if not shader_tex_desc.is_used:
				continue
			
			# it is used, figure out the slot it is used for
			for extra in extra_datas:
				if extra.integer_data == shader_tex_desc.map_index:
					shader_name = extra.name
					break
			else:
				self.nif_import.warning("No slot for shader texture %s."
										% shader_tex_desc.texture_data.source.file_name)
				continue
			try:
				extra_shader_index = (self.nif_import.EXTRA_SHADER_TEXTURES.index(shader_name))
			except ValueError:
				# shader_name not in self.EXTRA_SHADER_TEXTURES
				self.nif_import.warning(
					"No slot for shader texture %s."
					% shader_tex_desc.texture_data.source.file_name)
				continue
			
			self.import_shader_by_type(extra_shader_index)
			
	def import_shader_by_type(extra_shader_index):
		if extra_shader_index == 0:
			# EnvironmentMapIndex
			if shader_tex_desc.texture_data.source.file_name.lower().startswith("rrt_engine_env_map"):
				# sid meier's railroads: env map generated by engine
				# we can skip this
				print("Ignoring Env Map as generated by Engine")
			# XXX todo, civ4 uses this
			self.nif_import.warning("Skipping environment map texture.")
		elif extra_shader_index == 1:
			# NormalMapIndex
			bumpTexDesc = shader_tex_desc.texture_data
		elif extra_shader_index == 2:
			# SpecularIntensityIndex
			glossTexDesc = shader_tex_desc.texture_data
		elif extra_shader_index == 3:
			# EnvironmentIntensityIndex (this is reflection)
			refTexDesc = shader_tex_desc.texture_data
		elif extra_shader_index == 4:
			# LightCubeMapIndex
			if shader_tex_desc.texture_data.source.file_name.lower().startswith("rrt_cube_light_map"):
				# sid meier's railroads: light map generated by engine
				# we can skip this
				print("Ignoring Env Map as generated by Engine")
			self.nif_import.warning("Skipping light cube texture.")
		elif extra_shader_index == 5:
			# ShadowTextureIndex
			self.nif_import.warning("Skipping shadow texture.")
		
		
	def import_bsshaderproperty(b_mat, bsShaderProperty):
		baseTexFile = bsShaderProperty.texture_set.textures[0]
		if baseTexFile:
			self.import_diffuse_texture(b_mat, baseTexFile)
			
		bumpTexFile = bsShaderProperty.texture_set.textures[1]
		if n_texture_prop.has_bump_map_texture:
			self.import_bump_texture(b_mat, n_texture_prop)
		
		glowTexFile = bsShaderProperty.texture_set.textures[2]
		if n_texture_prop.has_glow_texture:
			self.import_glow_texture(b_mat, n_texture_prop)			
							
											
	def import_texture_effect(b_mat, textureEffect):
		diffuse_texture = n_textureDesc.base_texture
		
		b_mat_texslot = b_mat.texture_slots.add()
		b_mat_texslot.texture = self.textureloader.import_texture_source(diffuse_texture.source)
		b_mat_texslot.use = True

		# Influence mapping
		
		# Mapping
		b_mat_texslot.texture_coords = 'UV'
		b_mat_texslot.uv_layer = self.get_uv_layer_name(diffuse_texture.uv_set)
		
		# Influence
		b_mat_texslot.use_map_color_diffuse = True
		b_mat_texslot.blend_type = self.get_b_blend_type_from_n_apply_mode(
                n_textureDesc.apply_mode)
		
# 		if(n_alpha_prop):
# 			b_mat_texslot.use_map_alpha
		# update: needed later
		base_texture = b_mat_texslot
# 		
# 		envmapTexture = self.textureloader.import_texture_source(textureEffect.source_texture)
# 		if envmapTexture:
# 			# set the texture to use face reflection coordinates
# 			texco = 'REFLECTION'
# 			# map the texture to the base color channel
# 			mapto = FIXME.use_map_color_diffuse
# 			# set the texture for the material
# 			material.setTexture(3, envmapTexture, texco, mapto)
# 			menvmapTexture = material.getTextures()[3]
# 			menvmapTexture.blend_type = 'ADD'


	def import_diffuse_texture(self, b_mat, n_textureDesc):
		diffuse_texture = n_textureDesc.base_texture
		
		b_mat_texslot = b_mat.texture_slots.add()
		b_mat_texslot.texture = self.textureloader.import_texture_source(diffuse_texture.source)
		b_mat_texslot.use = True

		# Influence mapping
		
		# Mapping
		b_mat_texslot.texture_coords = 'UV'
		b_mat_texslot.uv_layer = self.get_uv_layer_name(diffuse_texture.uv_set)
		
		# Influence
		b_mat_texslot.use_map_color_diffuse = True
		b_mat_texslot.blend_type = self.get_b_blend_type_from_n_apply_mode(
                n_textureDesc.apply_mode)
		
# 		if(n_alpha_prop):
# 			b_mat_texslot.use_map_alpha
		# update: needed later
		base_texture = b_mat_texslot


	def import_bump_texture(self, b_mat, n_textureDesc):
		bumpmap_texture = n_textureDesc.bump_map_texture
		
		b_mat_texslot = b_mat.texture_slots.add()
		b_mat_texslot.texture = self.textureloader.import_texture_source(bumpmap_texture.source)
		b_mat_texslot.use = True
		
		# Influence mapping
		b_mat_texslot.texture.use_normal_map = False # causes artifacts otherwise.
		b_mat_texslot.use_map_color_diffuse = False
		
		# Mapping
		b_mat_texslot.texture_coords = 'UV'
		b_mat_texslot.uv_layer = self.get_uv_layer_name(bumpmap_texture.uv_set)
		
		# Influence
		b_mat_texslot.use_map_normal = True
		b_mat_texslot.blend_type = self.get_b_blend_type_from_n_apply_mode(
                n_textureDesc.apply_mode)
		
# 		if(n_alpha_prop):
# 			b_mat_texslot.use_map_alpha
		
		# update: needed later
		
		
	def import_glow_texture(self, b_mat, n_textureDesc):
		glow_texture = n_textureDesc.glow_texture
		
		b_mat_texslot = b_mat.texture_slots.add()
		b_mat_texslot.texture = self.textureloader.import_texture_source(glow_texture.source)
		b_mat_texslot.use = True
		
		# Influence mapping
		b_mat_texslot.texture.use_alpha = False
		b_mat_texslot.use_map_color_diffuse = False
		
		
		# Mapping
		b_mat_texslot.texture_coords = 'UV'
		b_mat_texslot.uv_layer = self.get_uv_layer_name(glow_texture.uv_set)
		
		# Influence
		b_mat_texslot.use_map_emit = True
		b_mat_texslot.blend_type = self.get_b_blend_type_from_n_apply_mode(
                n_textureDesc.apply_mode)
		
# 		if(n_alpha_prop):
# 			b_mat_texslot.use_map_alpha
			
		# update: needed later


	def import_gloss_texture(self, b_mat, n_textureDesc):
		gloss_texture = n_textureDesc.base_texture
		
		b_mat_texslot = b_mat.texture_slots.create(0)
		b_mat_texslot.texture = self.import_texture_source(glossTexDesc.source)
		b_mat_texslot.use = True

		# Influence mapping
		
		# Mapping
		b_mat_texslot.texture_coords = 'UV'
		b_mat_texslot.uv_layer = self.get_uv_layer_name(gloss_texture.uv_set)
		
		# Influence
		b_mat_texslot.use_map_color_diffuse = True
		b_mat_texslot.blend_type = self.get_b_blend_type_from_n_apply_mode(
                n_textureDesc.apply_mode)
		
# 		if(n_alpha_prop):
# 			b_mat_texslot.use_map_alpha
		# update: needed later
		base_texture = b_mat_texslot
		
		
# 		gloss_texture = 
# 		if gloss_texture:
# 			# set the texture to use face UV coordinates
# 			texco = 'UV'
# 			# map the texture to the specularity channel
# 			mapto = FIXME.use_map_specular
# 			# set the texture for the material
# 			material.setTexture(4, gloss_texture, texco, mapto)
# 			mgloss_texture = material.getTextures()[4]
# 			mgloss_texture.uv_layer = self.get_uv_layer_name(glossTexDesc.uv_set)
			
			
	def import_dark_texture(self, b_mat, n_textureDesc):
		dark_texture = n_textureDesc.base_texture
		
		b_mat_texslot = b_mat.texture_slots.add()
		b_mat_texslot.texture = self.textureloader.import_texture_source(dark_texture.source)
		b_mat_texslot.use = True

		# Influence mapping
		
		# Mapping
		b_mat_texslot.texture_coords = 'UV'
		b_mat_texslot.uv_layer = self.get_uv_layer_name(dark_texture.uv_set)
		
		# Influence
		b_mat_texslot.use_map_color_diffuse = True
		b_mat_texslot.blend_type = self.get_b_blend_type_from_n_apply_mode(
                n_textureDesc.apply_mode)
		
# 		if(n_alpha_prop):
# 			b_mat_texslot.use_map_alpha
		# update: needed later
		
# 		dark_texture = self.textureloader.import_texture_source(darkTexDesc.source)
# 		if dark_texture:
# 			# set the texture to use face UV coordinates
# 			texco = 'UV'
# 			# map the texture to the COL channel
# 			mapto = FIXME.use_map_color_diffuse
# 			# set the texture for the material
# 			material.setTexture(5, dark_texture, texco, mapto)
# 			mdark_texture = material.getTextures()[5]
# 			mdark_texture.uv_layer = self.get_uv_layer_name(darkTexDesc.uv_set)
# 			# set blend mode to "DARKEN"
# 			mdark_texture.blend_type = 'DARKEN'
		

	def import_detail_texture(self, b_mat, n_textureDesc):
		detail_texture = n_textureDesc.base_texture
		
		b_mat_texslot = b_mat.texture_slots.add()
		b_mat_texslot.texture = self.textureloader.import_texture_source(detail_texture.source)
		b_mat_texslot.use = True

		# Influence mapping
		
		# Mapping
		b_mat_texslot.texture_coords = 'UV'
		b_mat_texslot.uv_layer = self.get_uv_layer_name(detail_texture.uv_set)
		
		# Influence
		b_mat_texslot.use_map_color_diffuse = True
		b_mat_texslot.blend_type = self.get_b_blend_type_from_n_apply_mode(
                n_textureDesc.apply_mode)
		
# 		if(n_alpha_prop):
# 			b_mat_texslot.use_map_alpha
		# update: needed later
		
# 		detail_texture = self.textureloader.import_texture_source(detailTexDesc.source)
# 		if detail_texture:
# 			# import detail texture as extra base texture
# 			# set the texture to use face UV coordinates
# 			texco = 'UV'
# 			# map the texture to the COL channel
# 			mapto = FIXME.use_map_color_diffuse
# 			# set the texture for the material
# 			material.setTexture(6, detail_texture, texco, mapto)
# 			mdetail_texture = material.getTextures()[6]
# 			mdetail_texture.uv_layer = self.get_uv_layer_name(detailTexDesc.uv_set)

	def import_reflection_texture(self, b_mat, n_textureDesc):
		reflection_texture = n_textureDesc.base_texture
		
		b_mat_texslot = b_mat.texture_slots.add()
		b_mat_texslot.texture = self.textureloader.import_texture_source(reflection_texture.source)
		b_mat_texslot.use = True

		# Influence mapping
		
		# Mapping
		b_mat_texslot.texture_coords = 'UV'
		b_mat_texslot.uv_layer = self.get_uv_layer_name(reflection_texture.uv_set)
		
		# Influence
		b_mat_texslot.use_map_color_diffuse = True
		b_mat_texslot.blend_type = self.get_b_blend_type_from_n_apply_mode(
                n_textureDesc.apply_mode)
		
# 		if(n_alpha_prop):
# 			b_mat_texslot.use_map_alpha
		# update: needed later
		
		
# 		refTexture = self.textureloader.import_texture_source(refTexDesc.source)
# 		if refTexture:
# 			# set the texture to use face UV coordinates
# 			texco = 'UV'
# 			# map the texture to the base color and emit channel
# 			mapto = Blender.Texture.MapTo.REF
# 			# set the texture for the material
# 			material.setTexture(7, refTexture, texco, mapto)
# 			mrefTexture = material.getTextures()[7]
# 			mrefTexture.uv_layer = self.get_uv_layer_name(refTexDesc.uv_set)

		
	def get_b_blend_type_from_n_apply_mode(self, n_apply_mode):
		# TODO - Check out n_apply_modes
		if n_apply_mode == NifFormat.ApplyMode.APPLY_MODULATE:
			return "MIX"
        # TODO - These seem unsupported by Blender, check
		elif n_apply_mode == NifFormat.ApplyMode.APPLY_REPLACE:
			return "MIX"
		elif n_apply_mode == NifFormat.ApplyMode.APPLY_DECAL:
			return "MIX"
		elif n_apply_mode == NifFormat.ApplyMode.APPLY_HILIGHT:
			return "LIGHTEN"
		elif n_apply_mode == NifFormat.ApplyMode.APPLY_HILIGHT2: # used by Oblivion for parallax
			return "MULTIPLY"
		self.nif_import.warning(
			"Unknown apply mode (%i) in material,"
			" using blend type 'MIX'" % n_apply_mode)
		return "MIX"


	def get_uv_layer_name(self, uvset):
		return "UVMap.%03i" % uvset if uvset != 0 else "UVMap"
	
	
	def get_used_textslots(self, b_mat):
		# same material, should be pre-computed
		if self.b_mat == b_mat:
			return self.used_slots
		
		#first time through this material, lets precompute everything
		self.used_slots = [b_texslot for b_texslot in b_mat.texture_slots if b_texslot != None]
				
		self.diffusetextures = self.has_diffuse_textures(b_mat)
		self.bumpmaptextures = self.has_bumpmap_textures(b_mat)
		self.normalmaptextures = self.has_normalmap_textures(b_mat)
		self.glowtextures = self.has_glow_textures(b_mat)

		self.b_mat = b_mat
		
		return self.used_slots
		
	def has_diffuse_textures(self, b_mat):
		if(self.b_mat == b_mat):
			return self.diffusetextures

		for b_mat_texslot in self.get_used_textslots(b_mat):
			if b_mat_texslot.use and b_mat_texslot.use_map_color_diffuse:
				self.diffusetextures.append(b_mat_texslot)
		return self.diffusetextures	
	
	
	def has_glow_textures(self, b_mat):
		if(self.b_mat == b_mat):
			return self.glowtextures
		
		for b_mat_texslot in self.get_used_textslots(b_mat):
			if b_mat_texslot.use and b_mat_texslot.use_map_emit:
				self.glowtextures.append(b_mat_texslot)
		return self.glowtextures
				
	def has_bumpmap_textures(self, b_mat):
		if(self.b_mat == b_mat):
			return self.bumpmaptextures
		
		for b_mat_texslot in self.get_used_textslots(b_mat):
			if b_mat_texslot.use:
				if b_mat_texslot.texture.use_normal_map == False and \
				b_mat_texslot.use_map_color_diffuse == False:
					self.bumpmaptextures.append(b_mat_texslot)
		return self.bumpmaptextures
	
	
	
	def has_normalmap_textures(self, b_mat):
		if(self.b_mat == b_mat):
			return self.normalmaptextures
		
		for b_mat_texslot in self.get_used_textslots(b_mat):
			if b_mat_texslot.use:
				if b_mat_texslot.use_map_color_diffuse == False and \
				b_mat_texslot.texture.use_normal_map and b_mat_texslot.use_map_normal:
					self.normalmaptextures.append(b_mat_texslot)
		return self.normalmaptextures