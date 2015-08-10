# ./platform_config.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2015-08-10 12:29:37.907363 by PyXB version 1.2.5-DEV using Python 2.7.6.final.0
# Namespace AbsentNamespace0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:b39f50aa-3f4a-11e5-b0f5-001999a78414')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.5-DEV'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: word64Type
class word64Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'word64Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 3, 2)
    _Documentation = None
word64Type._CF_pattern = pyxb.binding.facets.CF_pattern()
word64Type._CF_pattern.addPattern(pattern='16#[0-9a-fA-F]{4}(_([0-9a-fA-F]{4})){0,3}#')
word64Type._InitializeFacetMap(word64Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'word64Type', word64Type)
_module_typeBindings.word64Type = word64Type

# Atomic simple type: byteType
class byteType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'byteType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 18, 2)
    _Documentation = None
byteType._CF_pattern = pyxb.binding.facets.CF_pattern()
byteType._CF_pattern.addPattern(pattern='16#[0-9a-fA-F]{2}#')
byteType._InitializeFacetMap(byteType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'byteType', byteType)
_module_typeBindings.byteType = byteType

# Atomic simple type: booleanType
class booleanType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'booleanType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 23, 2)
    _Documentation = None
booleanType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=booleanType, enum_prefix=None)
booleanType.true = booleanType._CF_enumeration.addEnumeration(unicode_value='true', tag='true')
booleanType.false = booleanType._CF_enumeration.addEnumeration(unicode_value='false', tag='false')
booleanType._InitializeFacetMap(booleanType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'booleanType', booleanType)
_module_typeBindings.booleanType = booleanType

# Atomic simple type: nameType
class nameType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'nameType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 29, 2)
    _Documentation = None
nameType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
nameType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(63))
nameType._InitializeFacetMap(nameType._CF_minLength,
   nameType._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'nameType', nameType)
_module_typeBindings.nameType = nameType

# Atomic simple type: noneType
class noneType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'noneType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 35, 2)
    _Documentation = None
noneType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=noneType, enum_prefix=None)
noneType.none = noneType._CF_enumeration.addEnumeration(unicode_value='none', tag='none')
noneType._InitializeFacetMap(noneType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'noneType', noneType)
_module_typeBindings.noneType = noneType

# Atomic simple type: pciDeviceNumberType
class pciDeviceNumberType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'pciDeviceNumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 56, 2)
    _Documentation = None
pciDeviceNumberType._CF_pattern = pyxb.binding.facets.CF_pattern()
pciDeviceNumberType._CF_pattern.addPattern(pattern='16#[0|1][0-9a-fA-F]#')
pciDeviceNumberType._InitializeFacetMap(pciDeviceNumberType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'pciDeviceNumberType', pciDeviceNumberType)
_module_typeBindings.pciDeviceNumberType = pciDeviceNumberType

# Atomic simple type: pciFunctionNumberType
class pciFunctionNumberType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'pciFunctionNumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 61, 2)
    _Documentation = None
pciFunctionNumberType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=pciFunctionNumberType, value=pyxb.binding.datatypes.nonNegativeInteger(7))
pciFunctionNumberType._InitializeFacetMap(pciFunctionNumberType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'pciFunctionNumberType', pciFunctionNumberType)
_module_typeBindings.pciFunctionNumberType = pciFunctionNumberType

# Atomic simple type: vmxTimerRateType
class vmxTimerRateType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'vmxTimerRateType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 77, 2)
    _Documentation = None
vmxTimerRateType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=vmxTimerRateType, value=pyxb.binding.datatypes.nonNegativeInteger(31))
vmxTimerRateType._InitializeFacetMap(vmxTimerRateType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'vmxTimerRateType', vmxTimerRateType)
_module_typeBindings.vmxTimerRateType = vmxTimerRateType

# Atomic simple type: vectorType
class vectorType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'vectorType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 94, 2)
    _Documentation = None
vectorType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=vectorType, value=pyxb.binding.datatypes.nonNegativeInteger(255))
vectorType._InitializeFacetMap(vectorType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'vectorType', vectorType)
_module_typeBindings.vectorType = vectorType

# Atomic simple type: irqNumberType
class irqNumberType (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'irqNumberType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 99, 2)
    _Documentation = None
irqNumberType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=irqNumberType, value=pyxb.binding.datatypes.nonNegativeInteger(220))
irqNumberType._InitializeFacetMap(irqNumberType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'irqNumberType', irqNumberType)
_module_typeBindings.irqNumberType = irqNumberType

# Atomic simple type: cachingType
class cachingType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'cachingType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 153, 2)
    _Documentation = None
cachingType._CF_pattern = pyxb.binding.facets.CF_pattern()
cachingType._CF_pattern.addPattern(pattern='UC|WC|WT|WB|WP')
cachingType._InitializeFacetMap(cachingType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'cachingType', cachingType)
_module_typeBindings.cachingType = cachingType

# Atomic simple type: memoryKindType
class memoryKindType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'memoryKindType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 158, 2)
    _Documentation = None
memoryKindType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=memoryKindType, enum_prefix=None)
memoryKindType.system = memoryKindType._CF_enumeration.addEnumeration(unicode_value='system', tag='system')
memoryKindType.system_vmxon = memoryKindType._CF_enumeration.addEnumeration(unicode_value='system_vmxon', tag='system_vmxon')
memoryKindType.system_vmcs = memoryKindType._CF_enumeration.addEnumeration(unicode_value='system_vmcs', tag='system_vmcs')
memoryKindType.system_iobm = memoryKindType._CF_enumeration.addEnumeration(unicode_value='system_iobm', tag='system_iobm')
memoryKindType.system_msrbm = memoryKindType._CF_enumeration.addEnumeration(unicode_value='system_msrbm', tag='system_msrbm')
memoryKindType.system_msrstore = memoryKindType._CF_enumeration.addEnumeration(unicode_value='system_msrstore', tag='system_msrstore')
memoryKindType.system_pt = memoryKindType._CF_enumeration.addEnumeration(unicode_value='system_pt', tag='system_pt')
memoryKindType.system_vtd_root = memoryKindType._CF_enumeration.addEnumeration(unicode_value='system_vtd_root', tag='system_vtd_root')
memoryKindType.system_vtd_context = memoryKindType._CF_enumeration.addEnumeration(unicode_value='system_vtd_context', tag='system_vtd_context')
memoryKindType.kernel = memoryKindType._CF_enumeration.addEnumeration(unicode_value='kernel', tag='kernel')
memoryKindType.kernel_binary = memoryKindType._CF_enumeration.addEnumeration(unicode_value='kernel_binary', tag='kernel_binary')
memoryKindType.kernel_interface = memoryKindType._CF_enumeration.addEnumeration(unicode_value='kernel_interface', tag='kernel_interface')
memoryKindType.kernel_vtd_ir = memoryKindType._CF_enumeration.addEnumeration(unicode_value='kernel_vtd_ir', tag='kernel_vtd_ir')
memoryKindType.subject = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject', tag='subject')
memoryKindType.subject_info = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_info', tag='subject_info')
memoryKindType.subject_state = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_state', tag='subject_state')
memoryKindType.subject_binary = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_binary', tag='subject_binary')
memoryKindType.subject_channel = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_channel', tag='subject_channel')
memoryKindType.subject_initrd = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_initrd', tag='subject_initrd')
memoryKindType.subject_bios = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_bios', tag='subject_bios')
memoryKindType.subject_acpi_rsdp = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_acpi_rsdp', tag='subject_acpi_rsdp')
memoryKindType.subject_acpi_xsdt = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_acpi_xsdt', tag='subject_acpi_xsdt')
memoryKindType.subject_acpi_fadt = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_acpi_fadt', tag='subject_acpi_fadt')
memoryKindType.subject_acpi_dsdt = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_acpi_dsdt', tag='subject_acpi_dsdt')
memoryKindType.subject_zeropage = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_zeropage', tag='subject_zeropage')
memoryKindType.subject_device = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_device', tag='subject_device')
memoryKindType.subject_timer = memoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_timer', tag='subject_timer')
memoryKindType._InitializeFacetMap(memoryKindType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'memoryKindType', memoryKindType)
_module_typeBindings.memoryKindType = memoryKindType

# Atomic simple type: word32Type
class word32Type (word64Type):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'word32Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 8, 2)
    _Documentation = None
word32Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(13))
word32Type._InitializeFacetMap(word32Type._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'word32Type', word32Type)
_module_typeBindings.word32Type = word32Type

# Atomic simple type: word16Type
class word16Type (word64Type):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'word16Type')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 13, 2)
    _Documentation = None
word16Type._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(8))
word16Type._InitializeFacetMap(word16Type._CF_length)
Namespace.addCategoryObject('typeBinding', 'word16Type', word16Type)
_module_typeBindings.word16Type = word16Type

# Atomic simple type: memorySizeType
class memorySizeType (word64Type):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'memorySizeType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 143, 2)
    _Documentation = None
memorySizeType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'memorySizeType', memorySizeType)
_module_typeBindings.memorySizeType = memorySizeType

# Atomic simple type: alignmentType
class alignmentType (word64Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'alignmentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 146, 2)
    _Documentation = None
alignmentType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=alignmentType, enum_prefix=None)
alignmentType.n161000 = alignmentType._CF_enumeration.addEnumeration(unicode_value='16#1000#', tag='n161000')
alignmentType.n160020_0000 = alignmentType._CF_enumeration.addEnumeration(unicode_value='16#0020_0000#', tag='n160020_0000')
alignmentType.n164000_0000 = alignmentType._CF_enumeration.addEnumeration(unicode_value='16#4000_0000#', tag='n164000_0000')
alignmentType._InitializeFacetMap(alignmentType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'alignmentType', alignmentType)
_module_typeBindings.alignmentType = alignmentType

# Union simple type: optionalOffsetType
# superclasses pyxb.binding.datatypes.anySimpleType
class optionalOffsetType (pyxb.binding.basis.STD_union):

    """Simple type that is a union of word64Type, noneType."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'optionalOffsetType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 205, 2)
    _Documentation = None

    _MemberTypes = ( word64Type, noneType, )
optionalOffsetType._CF_pattern = pyxb.binding.facets.CF_pattern()
optionalOffsetType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=optionalOffsetType)
optionalOffsetType.none = 'none'                  # originally noneType.none
optionalOffsetType._InitializeFacetMap(optionalOffsetType._CF_pattern,
   optionalOffsetType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'optionalOffsetType', optionalOffsetType)
_module_typeBindings.optionalOffsetType = optionalOffsetType

# Atomic simple type: subjectMemoryKindType
class subjectMemoryKindType (memoryKindType, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'subjectMemoryKindType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 256, 2)
    _Documentation = None
subjectMemoryKindType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=subjectMemoryKindType, enum_prefix=None)
subjectMemoryKindType.subject = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject', tag='subject')
subjectMemoryKindType.subject_info = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_info', tag='subject_info')
subjectMemoryKindType.subject_state = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_state', tag='subject_state')
subjectMemoryKindType.subject_binary = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_binary', tag='subject_binary')
subjectMemoryKindType.subject_channel = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_channel', tag='subject_channel')
subjectMemoryKindType.subject_initrd = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_initrd', tag='subject_initrd')
subjectMemoryKindType.subject_bios = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_bios', tag='subject_bios')
subjectMemoryKindType.subject_acpi_rsdp = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_acpi_rsdp', tag='subject_acpi_rsdp')
subjectMemoryKindType.subject_acpi_xsdt = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_acpi_xsdt', tag='subject_acpi_xsdt')
subjectMemoryKindType.subject_acpi_fadt = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_acpi_fadt', tag='subject_acpi_fadt')
subjectMemoryKindType.subject_acpi_dsdt = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_acpi_dsdt', tag='subject_acpi_dsdt')
subjectMemoryKindType.subject_zeropage = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_zeropage', tag='subject_zeropage')
subjectMemoryKindType.subject_device = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_device', tag='subject_device')
subjectMemoryKindType.subject_timer = subjectMemoryKindType._CF_enumeration.addEnumeration(unicode_value='subject_timer', tag='subject_timer')
subjectMemoryKindType._InitializeFacetMap(subjectMemoryKindType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'subjectMemoryKindType', subjectMemoryKindType)
_module_typeBindings.subjectMemoryKindType = subjectMemoryKindType

# Complex type capabilitiesType with content type ELEMENT_ONLY
class capabilitiesType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type capabilitiesType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'capabilitiesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 82, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element capability uses Python identifier capability
    __capability = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'capability'), 'capability', '__AbsentNamespace0_capabilitiesType_capability', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 84, 3), )

    
    capability = property(__capability.value, __capability.set, None, None)

    _ElementMap.update({
        __capability.name() : __capability
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.capabilitiesType = capabilitiesType
Namespace.addCategoryObject('typeBinding', 'capabilitiesType', capabilitiesType)


# Complex type capabilityType with content type SIMPLE
class capabilityType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type capabilityType with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'capabilityType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 87, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_capabilityType_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 90, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 90, 4)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.capabilityType = capabilityType
Namespace.addCategoryObject('typeBinding', 'capabilityType', capabilityType)


# Complex type devicesRefType with content type ELEMENT_ONLY
class devicesRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type devicesRefType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'devicesRefType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 113, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element device uses Python identifier device
    __device = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'device'), 'device', '__AbsentNamespace0_devicesRefType_device', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 115, 3), )

    
    device = property(__device.value, __device.set, None, None)

    _ElementMap.update({
        __device.name() : __device
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.devicesRefType = devicesRefType
Namespace.addCategoryObject('typeBinding', 'devicesRefType', devicesRefType)


# Complex type resourcesType with content type ELEMENT_ONLY
class resourcesType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type resourcesType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'resourcesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 137, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element irq uses Python identifier irq
    __irq = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'irq'), 'irq', '__AbsentNamespace0_resourcesType_irq', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 139, 3), )

    
    irq = property(__irq.value, __irq.set, None, None)

    
    # Element ioPort uses Python identifier ioPort
    __ioPort = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ioPort'), 'ioPort', '__AbsentNamespace0_resourcesType_ioPort', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 140, 3), )

    
    ioPort = property(__ioPort.value, __ioPort.set, None, None)

    _ElementMap.update({
        __irq.name() : __irq,
        __ioPort.name() : __ioPort
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.resourcesType = resourcesType
Namespace.addCategoryObject('typeBinding', 'resourcesType', resourcesType)


# Complex type memRegionsType with content type ELEMENT_ONLY
class memRegionsType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type memRegionsType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'memRegionsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 211, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element memory uses Python identifier memory
    __memory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'memory'), 'memory', '__AbsentNamespace0_memRegionsType_memory', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 213, 3), )

    
    memory = property(__memory.value, __memory.set, None, None)

    _ElementMap.update({
        __memory.name() : __memory
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.memRegionsType = memRegionsType
Namespace.addCategoryObject('typeBinding', 'memRegionsType', memRegionsType)


# Complex type memoryRefsType with content type ELEMENT_ONLY
class memoryRefsType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type memoryRefsType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'memoryRefsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 216, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element memory uses Python identifier memory
    __memory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'memory'), 'memory', '__AbsentNamespace0_memoryRefsType_memory', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 218, 3), )

    
    memory = property(__memory.value, __memory.set, None, None)

    _ElementMap.update({
        __memory.name() : __memory
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.memoryRefsType = memoryRefsType
Namespace.addCategoryObject('typeBinding', 'memoryRefsType', memoryRefsType)


# Complex type physicalMemoryType with content type ELEMENT_ONLY
class physicalMemoryType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type physicalMemoryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'physicalMemoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 274, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element memoryBlock uses Python identifier memoryBlock
    __memoryBlock = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'memoryBlock'), 'memoryBlock', '__AbsentNamespace0_physicalMemoryType_memoryBlock', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 276, 3), )

    
    memoryBlock = property(__memoryBlock.value, __memoryBlock.set, None, None)

    _ElementMap.update({
        __memoryBlock.name() : __memoryBlock
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.physicalMemoryType = physicalMemoryType
Namespace.addCategoryObject('typeBinding', 'physicalMemoryType', physicalMemoryType)


# Complex type platformType with content type ELEMENT_ONLY
class platformType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type platformType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'platformType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 279, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element processor uses Python identifier processor
    __processor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'processor'), 'processor', '__AbsentNamespace0_platformType_processor', False, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 281, 3), )

    
    processor = property(__processor.value, __processor.set, None, None)

    
    # Element memory uses Python identifier memory
    __memory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'memory'), 'memory', '__AbsentNamespace0_platformType_memory', False, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 282, 3), )

    
    memory = property(__memory.value, __memory.set, None, None)

    
    # Element devices uses Python identifier devices
    __devices = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'devices'), 'devices', '__AbsentNamespace0_platformType_devices', False, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 283, 3), )

    
    devices = property(__devices.value, __devices.set, None, None)

    _ElementMap.update({
        __processor.name() : __processor,
        __memory.name() : __memory,
        __devices.name() : __devices
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.platformType = platformType
Namespace.addCategoryObject('typeBinding', 'platformType', platformType)


# Complex type deviceType with content type ELEMENT_ONLY
class deviceType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type deviceType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'deviceType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 40, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element pci uses Python identifier pci
    __pci = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'pci'), 'pci', '__AbsentNamespace0_deviceType_pci', False, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 42, 3), )

    
    pci = property(__pci.value, __pci.set, None, None)

    
    # Element irq uses Python identifier irq
    __irq = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'irq'), 'irq', '__AbsentNamespace0_deviceType_irq', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 43, 3), )

    
    irq = property(__irq.value, __irq.set, None, None)

    
    # Element memory uses Python identifier memory
    __memory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'memory'), 'memory', '__AbsentNamespace0_deviceType_memory', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 44, 3), )

    
    memory = property(__memory.value, __memory.set, None, None)

    
    # Element ioPort uses Python identifier ioPort
    __ioPort = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ioPort'), 'ioPort', '__AbsentNamespace0_deviceType_ioPort', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 45, 3), )

    
    ioPort = property(__ioPort.value, __ioPort.set, None, None)

    
    # Element capabilities uses Python identifier capabilities
    __capabilities = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'capabilities'), 'capabilities', '__AbsentNamespace0_deviceType_capabilities', False, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 46, 3), )

    
    capabilities = property(__capabilities.value, __capabilities.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_deviceType_name', _module_typeBindings.nameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 48, 2)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 48, 2)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute shared uses Python identifier shared
    __shared = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'shared'), 'shared', '__AbsentNamespace0_deviceType_shared', _module_typeBindings.booleanType, required=True)
    __shared._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 49, 2)
    __shared._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 49, 2)
    
    shared = property(__shared.value, __shared.set, None, None)

    _ElementMap.update({
        __pci.name() : __pci,
        __irq.name() : __irq,
        __memory.name() : __memory,
        __ioPort.name() : __ioPort,
        __capabilities.name() : __capabilities
    })
    _AttributeMap.update({
        __name.name() : __name,
        __shared.name() : __shared
    })
_module_typeBindings.deviceType = deviceType
Namespace.addCategoryObject('typeBinding', 'deviceType', deviceType)


# Complex type pciType with content type EMPTY
class pciType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type pciType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'pciType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 51, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute bus uses Python identifier bus
    __bus = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'bus'), 'bus', '__AbsentNamespace0_pciType_bus', _module_typeBindings.byteType)
    __bus._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 52, 2)
    __bus._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 52, 2)
    
    bus = property(__bus.value, __bus.set, None, None)

    
    # Attribute device uses Python identifier device
    __device = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'device'), 'device', '__AbsentNamespace0_pciType_device', _module_typeBindings.pciDeviceNumberType)
    __device._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 53, 2)
    __device._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 53, 2)
    
    device = property(__device.value, __device.set, None, None)

    
    # Attribute function uses Python identifier function
    __function = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'function'), 'function', '__AbsentNamespace0_pciType_function', _module_typeBindings.pciFunctionNumberType)
    __function._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 54, 2)
    __function._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 54, 2)
    
    function = property(__function.value, __function.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __bus.name() : __bus,
        __device.name() : __device,
        __function.name() : __function
    })
_module_typeBindings.pciType = pciType
Namespace.addCategoryObject('typeBinding', 'pciType', pciType)


# Complex type devicesType with content type ELEMENT_ONLY
class devicesType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type devicesType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'devicesType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 66, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element device uses Python identifier device
    __device = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'device'), 'device', '__AbsentNamespace0_devicesType_device', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 68, 3), )

    
    device = property(__device.value, __device.set, None, None)

    
    # Attribute pciConfigAddress uses Python identifier pciConfigAddress
    __pciConfigAddress = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'pciConfigAddress'), 'pciConfigAddress', '__AbsentNamespace0_devicesType_pciConfigAddress', _module_typeBindings.word64Type)
    __pciConfigAddress._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 70, 2)
    __pciConfigAddress._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 70, 2)
    
    pciConfigAddress = property(__pciConfigAddress.value, __pciConfigAddress.set, None, None)

    _ElementMap.update({
        __device.name() : __device
    })
    _AttributeMap.update({
        __pciConfigAddress.name() : __pciConfigAddress
    })
_module_typeBindings.devicesType = devicesType
Namespace.addCategoryObject('typeBinding', 'devicesType', devicesType)


# Complex type processorType with content type EMPTY
class processorType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type processorType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'processorType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 72, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute logicalCpus uses Python identifier logicalCpus
    __logicalCpus = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'logicalCpus'), 'logicalCpus', '__AbsentNamespace0_processorType_logicalCpus', pyxb.binding.datatypes.positiveInteger, required=True)
    __logicalCpus._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 73, 2)
    __logicalCpus._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 73, 2)
    
    logicalCpus = property(__logicalCpus.value, __logicalCpus.set, None, None)

    
    # Attribute speed uses Python identifier speed
    __speed = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'speed'), 'speed', '__AbsentNamespace0_processorType_speed', pyxb.binding.datatypes.positiveInteger, required=True)
    __speed._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 74, 2)
    __speed._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 74, 2)
    
    speed = property(__speed.value, __speed.set, None, None)

    
    # Attribute vmxTimerRate uses Python identifier vmxTimerRate
    __vmxTimerRate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'vmxTimerRate'), 'vmxTimerRate', '__AbsentNamespace0_processorType_vmxTimerRate', _module_typeBindings.vmxTimerRateType, required=True)
    __vmxTimerRate._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 75, 2)
    __vmxTimerRate._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 75, 2)
    
    vmxTimerRate = property(__vmxTimerRate.value, __vmxTimerRate.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __logicalCpus.name() : __logicalCpus,
        __speed.name() : __speed,
        __vmxTimerRate.name() : __vmxTimerRate
    })
_module_typeBindings.processorType = processorType
Namespace.addCategoryObject('typeBinding', 'processorType', processorType)


# Complex type irqType with content type EMPTY
class irqType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type irqType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'irqType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 109, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_irqType_name', _module_typeBindings.nameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 110, 2)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 110, 2)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute number uses Python identifier number
    __number = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'number'), 'number', '__AbsentNamespace0_irqType_number', _module_typeBindings.irqNumberType, required=True)
    __number._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 111, 2)
    __number._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 111, 2)
    
    number = property(__number.value, __number.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __number.name() : __number
    })
_module_typeBindings.irqType = irqType
Namespace.addCategoryObject('typeBinding', 'irqType', irqType)


# Complex type deviceRefType with content type ELEMENT_ONLY
class deviceRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type deviceRefType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'deviceRefType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 118, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element pci uses Python identifier pci
    __pci = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'pci'), 'pci', '__AbsentNamespace0_deviceRefType_pci', False, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 120, 3), )

    
    pci = property(__pci.value, __pci.set, None, None)

    
    # Element memory uses Python identifier memory
    __memory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'memory'), 'memory', '__AbsentNamespace0_deviceRefType_memory', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 121, 3), )

    
    memory = property(__memory.value, __memory.set, None, None)

    
    # Element ioPort uses Python identifier ioPort
    __ioPort = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ioPort'), 'ioPort', '__AbsentNamespace0_deviceRefType_ioPort', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 122, 3), )

    
    ioPort = property(__ioPort.value, __ioPort.set, None, None)

    
    # Element irq uses Python identifier irq
    __irq = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'irq'), 'irq', '__AbsentNamespace0_deviceRefType_irq', True, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 123, 3), )

    
    irq = property(__irq.value, __irq.set, None, None)

    
    # Attribute logical uses Python identifier logical
    __logical = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'logical'), 'logical', '__AbsentNamespace0_deviceRefType_logical', _module_typeBindings.nameType, required=True)
    __logical._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 125, 2)
    __logical._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 125, 2)
    
    logical = property(__logical.value, __logical.set, None, None)

    
    # Attribute physical uses Python identifier physical
    __physical = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'physical'), 'physical', '__AbsentNamespace0_deviceRefType_physical', _module_typeBindings.nameType, required=True)
    __physical._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 126, 2)
    __physical._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 126, 2)
    
    physical = property(__physical.value, __physical.set, None, None)

    _ElementMap.update({
        __pci.name() : __pci,
        __memory.name() : __memory,
        __ioPort.name() : __ioPort,
        __irq.name() : __irq
    })
    _AttributeMap.update({
        __logical.name() : __logical,
        __physical.name() : __physical
    })
_module_typeBindings.deviceRefType = deviceRefType
Namespace.addCategoryObject('typeBinding', 'deviceRefType', deviceRefType)


# Complex type ioPortRefType with content type EMPTY
class ioPortRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type ioPortRefType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ioPortRefType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 128, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute logical uses Python identifier logical
    __logical = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'logical'), 'logical', '__AbsentNamespace0_ioPortRefType_logical', _module_typeBindings.nameType, required=True)
    __logical._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 129, 2)
    __logical._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 129, 2)
    
    logical = property(__logical.value, __logical.set, None, None)

    
    # Attribute physical uses Python identifier physical
    __physical = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'physical'), 'physical', '__AbsentNamespace0_ioPortRefType_physical', _module_typeBindings.nameType, required=True)
    __physical._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 130, 2)
    __physical._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 130, 2)
    
    physical = property(__physical.value, __physical.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __logical.name() : __logical,
        __physical.name() : __physical
    })
_module_typeBindings.ioPortRefType = ioPortRefType
Namespace.addCategoryObject('typeBinding', 'ioPortRefType', ioPortRefType)


# Complex type irqRefType with content type EMPTY
class irqRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type irqRefType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'irqRefType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 132, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute logical uses Python identifier logical
    __logical = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'logical'), 'logical', '__AbsentNamespace0_irqRefType_logical', _module_typeBindings.nameType, required=True)
    __logical._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 133, 2)
    __logical._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 133, 2)
    
    logical = property(__logical.value, __logical.set, None, None)

    
    # Attribute physical uses Python identifier physical
    __physical = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'physical'), 'physical', '__AbsentNamespace0_irqRefType_physical', _module_typeBindings.nameType, required=True)
    __physical._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 134, 2)
    __physical._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 134, 2)
    
    physical = property(__physical.value, __physical.set, None, None)

    
    # Attribute vector uses Python identifier vector
    __vector = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'vector'), 'vector', '__AbsentNamespace0_irqRefType_vector', _module_typeBindings.vectorType, required=True)
    __vector._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 135, 2)
    __vector._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 135, 2)
    
    vector = property(__vector.value, __vector.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __logical.name() : __logical,
        __physical.name() : __physical,
        __vector.name() : __vector
    })
_module_typeBindings.irqRefType = irqRefType
Namespace.addCategoryObject('typeBinding', 'irqRefType', irqRefType)


# Complex type fillContentType with content type EMPTY
class fillContentType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type fillContentType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fillContentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 208, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute pattern uses Python identifier pattern
    __pattern = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'pattern'), 'pattern', '__AbsentNamespace0_fillContentType_pattern', _module_typeBindings.byteType, required=True)
    __pattern._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 209, 2)
    __pattern._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 209, 2)
    
    pattern = property(__pattern.value, __pattern.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __pattern.name() : __pattern
    })
_module_typeBindings.fillContentType = fillContentType
Namespace.addCategoryObject('typeBinding', 'fillContentType', fillContentType)


# Complex type memRefType with content type EMPTY
class memRefType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type memRefType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'memRefType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 245, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute logical uses Python identifier logical
    __logical = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'logical'), 'logical', '__AbsentNamespace0_memRefType_logical', _module_typeBindings.nameType, required=True)
    __logical._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 222, 2)
    __logical._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 222, 2)
    
    logical = property(__logical.value, __logical.set, None, None)

    
    # Attribute physical uses Python identifier physical
    __physical = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'physical'), 'physical', '__AbsentNamespace0_memRefType_physical', _module_typeBindings.nameType, required=True)
    __physical._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 223, 2)
    __physical._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 223, 2)
    
    physical = property(__physical.value, __physical.set, None, None)

    
    # Attribute writable uses Python identifier writable
    __writable = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'writable'), 'writable', '__AbsentNamespace0_memRefType_writable', _module_typeBindings.booleanType, required=True)
    __writable._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 224, 2)
    __writable._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 224, 2)
    
    writable = property(__writable.value, __writable.set, None, None)

    
    # Attribute executable uses Python identifier executable
    __executable = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'executable'), 'executable', '__AbsentNamespace0_memRefType_executable', _module_typeBindings.booleanType, required=True)
    __executable._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 225, 2)
    __executable._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 225, 2)
    
    executable = property(__executable.value, __executable.set, None, None)

    
    # Attribute virtualAddress uses Python identifier virtualAddress
    __virtualAddress = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'virtualAddress'), 'virtualAddress', '__AbsentNamespace0_memRefType_virtualAddress', _module_typeBindings.word64Type)
    __virtualAddress._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 247, 2)
    __virtualAddress._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 247, 2)
    
    virtualAddress = property(__virtualAddress.value, __virtualAddress.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __logical.name() : __logical,
        __physical.name() : __physical,
        __writable.name() : __writable,
        __executable.name() : __executable,
        __virtualAddress.name() : __virtualAddress
    })
_module_typeBindings.memRefType = memRefType
Namespace.addCategoryObject('typeBinding', 'memRefType', memRefType)


# Complex type ioPortType with content type EMPTY
class ioPortType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type ioPortType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ioPortType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 104, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_ioPortType_name', _module_typeBindings.nameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 105, 2)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 105, 2)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'start'), 'start', '__AbsentNamespace0_ioPortType_start', _module_typeBindings.word16Type, required=True)
    __start._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 106, 2)
    __start._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 106, 2)
    
    start = property(__start.value, __start.set, None, None)

    
    # Attribute end uses Python identifier end
    __end = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'end'), 'end', '__AbsentNamespace0_ioPortType_end', _module_typeBindings.word16Type, required=True)
    __end._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 107, 2)
    __end._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 107, 2)
    
    end = property(__end.value, __end.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __start.name() : __start,
        __end.name() : __end
    })
_module_typeBindings.ioPortType = ioPortType
Namespace.addCategoryObject('typeBinding', 'ioPortType', ioPortType)


# Complex type memoryBlockBaseType with content type EMPTY
class memoryBlockBaseType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type memoryBlockBaseType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'memoryBlockBaseType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 189, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_memoryBlockBaseType_name', _module_typeBindings.nameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 190, 2)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 190, 2)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute physicalAddress uses Python identifier physicalAddress
    __physicalAddress = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'physicalAddress'), 'physicalAddress', '__AbsentNamespace0_memoryBlockBaseType_physicalAddress', _module_typeBindings.word64Type, required=True)
    __physicalAddress._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 191, 2)
    __physicalAddress._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 191, 2)
    
    physicalAddress = property(__physicalAddress.value, __physicalAddress.set, None, None)

    
    # Attribute size uses Python identifier size
    __size = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'size'), 'size', '__AbsentNamespace0_memoryBlockBaseType_size', _module_typeBindings.memorySizeType, required=True)
    __size._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 192, 2)
    __size._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 192, 2)
    
    size = property(__size.value, __size.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __physicalAddress.name() : __physicalAddress,
        __size.name() : __size
    })
_module_typeBindings.memoryBlockBaseType = memoryBlockBaseType
Namespace.addCategoryObject('typeBinding', 'memoryBlockBaseType', memoryBlockBaseType)


# Complex type fileContentType with content type EMPTY
class fileContentType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type fileContentType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fileContentType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 201, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute filename uses Python identifier filename
    __filename = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'filename'), 'filename', '__AbsentNamespace0_fileContentType_filename', pyxb.binding.datatypes.string, required=True)
    __filename._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 202, 2)
    __filename._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 202, 2)
    
    filename = property(__filename.value, __filename.set, None, None)

    
    # Attribute offset uses Python identifier offset
    __offset = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'offset'), 'offset', '__AbsentNamespace0_fileContentType_offset', _module_typeBindings.optionalOffsetType, required=True)
    __offset._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 203, 2)
    __offset._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 203, 2)
    
    offset = property(__offset.value, __offset.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __filename.name() : __filename,
        __offset.name() : __offset
    })
_module_typeBindings.fileContentType = fileContentType
Namespace.addCategoryObject('typeBinding', 'fileContentType', fileContentType)


# Complex type memoryBaseType with content type ELEMENT_ONLY
class memoryBaseType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type memoryBaseType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'memoryBaseType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 227, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element file uses Python identifier file
    __file = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'file'), 'file', '__AbsentNamespace0_memoryBaseType_file', False, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 229, 3), )

    
    file = property(__file.value, __file.set, None, None)

    
    # Element fill uses Python identifier fill
    __fill = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'fill'), 'fill', '__AbsentNamespace0_memoryBaseType_fill', False, pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 230, 3), )

    
    fill = property(__fill.value, __fill.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__AbsentNamespace0_memoryBaseType_name', _module_typeBindings.nameType, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 232, 2)
    __name._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 232, 2)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute size uses Python identifier size
    __size = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'size'), 'size', '__AbsentNamespace0_memoryBaseType_size', _module_typeBindings.memorySizeType, required=True)
    __size._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 233, 2)
    __size._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 233, 2)
    
    size = property(__size.value, __size.set, None, None)

    
    # Attribute caching uses Python identifier caching
    __caching = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'caching'), 'caching', '__AbsentNamespace0_memoryBaseType_caching', _module_typeBindings.cachingType, required=True)
    __caching._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 234, 2)
    __caching._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 234, 2)
    
    caching = property(__caching.value, __caching.set, None, None)

    _ElementMap.update({
        __file.name() : __file,
        __fill.name() : __fill
    })
    _AttributeMap.update({
        __name.name() : __name,
        __size.name() : __size,
        __caching.name() : __caching
    })
_module_typeBindings.memoryBaseType = memoryBaseType
Namespace.addCategoryObject('typeBinding', 'memoryBaseType', memoryBaseType)


# Complex type deviceMemoryType with content type EMPTY
class deviceMemoryType (memoryBlockBaseType):
    """Complex type deviceMemoryType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'deviceMemoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 194, 2)
    _ElementMap = memoryBlockBaseType._ElementMap.copy()
    _AttributeMap = memoryBlockBaseType._AttributeMap.copy()
    # Base type is memoryBlockBaseType
    
    # Attribute name inherited from memoryBlockBaseType
    
    # Attribute physicalAddress inherited from memoryBlockBaseType
    
    # Attribute size inherited from memoryBlockBaseType
    
    # Attribute caching uses Python identifier caching
    __caching = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'caching'), 'caching', '__AbsentNamespace0_deviceMemoryType_caching', _module_typeBindings.cachingType, required=True)
    __caching._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 197, 4)
    __caching._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 197, 4)
    
    caching = property(__caching.value, __caching.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __caching.name() : __caching
    })
_module_typeBindings.deviceMemoryType = deviceMemoryType
Namespace.addCategoryObject('typeBinding', 'deviceMemoryType', deviceMemoryType)


# Complex type memoryType with content type ELEMENT_ONLY
class memoryType (memoryBaseType):
    """Complex type memoryType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'memoryType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 236, 2)
    _ElementMap = memoryBaseType._ElementMap.copy()
    _AttributeMap = memoryBaseType._AttributeMap.copy()
    # Base type is memoryBaseType
    
    # Element file (file) inherited from memoryBaseType
    
    # Element fill (fill) inherited from memoryBaseType
    
    # Attribute name inherited from memoryBaseType
    
    # Attribute size inherited from memoryBaseType
    
    # Attribute caching inherited from memoryBaseType
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__AbsentNamespace0_memoryType_type', _module_typeBindings.subjectMemoryKindType)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 239, 4)
    __type._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 239, 4)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute alignment uses Python identifier alignment
    __alignment = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'alignment'), 'alignment', '__AbsentNamespace0_memoryType_alignment', _module_typeBindings.alignmentType)
    __alignment._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 240, 4)
    __alignment._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 240, 4)
    
    alignment = property(__alignment.value, __alignment.set, None, None)

    
    # Attribute physicalAddress uses Python identifier physicalAddress
    __physicalAddress = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'physicalAddress'), 'physicalAddress', '__AbsentNamespace0_memoryType_physicalAddress', _module_typeBindings.word64Type)
    __physicalAddress._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 241, 4)
    __physicalAddress._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 241, 4)
    
    physicalAddress = property(__physicalAddress.value, __physicalAddress.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type,
        __alignment.name() : __alignment,
        __physicalAddress.name() : __physicalAddress
    })
_module_typeBindings.memoryType = memoryType
Namespace.addCategoryObject('typeBinding', 'memoryType', memoryType)


# Complex type memoryBlockType with content type EMPTY
class memoryBlockType (memoryBlockBaseType):
    """Complex type memoryBlockType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'memoryBlockType')
    _XSDLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 249, 2)
    _ElementMap = memoryBlockBaseType._ElementMap.copy()
    _AttributeMap = memoryBlockBaseType._AttributeMap.copy()
    # Base type is memoryBlockBaseType
    
    # Attribute name inherited from memoryBlockBaseType
    
    # Attribute physicalAddress inherited from memoryBlockBaseType
    
    # Attribute size inherited from memoryBlockBaseType
    
    # Attribute allocatable uses Python identifier allocatable
    __allocatable = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'allocatable'), 'allocatable', '__AbsentNamespace0_memoryBlockType_allocatable', _module_typeBindings.booleanType)
    __allocatable._DeclarationLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 252, 4)
    __allocatable._UseLocation = pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 252, 4)
    
    allocatable = property(__allocatable.value, __allocatable.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __allocatable.name() : __allocatable
    })
_module_typeBindings.memoryBlockType = memoryBlockType
Namespace.addCategoryObject('typeBinding', 'memoryBlockType', memoryBlockType)


platform = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'platform'), platformType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 286, 2))
Namespace.addCategoryObject('elementBinding', platform.name().localName(), platform)



capabilitiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'capability'), capabilityType, scope=capabilitiesType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 84, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(capabilitiesType._UseForTag(pyxb.namespace.ExpandedName(None, 'capability')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 84, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
capabilitiesType._Automaton = _BuildAutomaton()




devicesRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'device'), deviceRefType, scope=devicesRefType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 115, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 115, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(devicesRefType._UseForTag(pyxb.namespace.ExpandedName(None, 'device')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 115, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
devicesRefType._Automaton = _BuildAutomaton_()




resourcesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'irq'), irqType, scope=resourcesType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 139, 3)))

resourcesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ioPort'), ioPortType, scope=resourcesType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 140, 3)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 139, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 140, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(resourcesType._UseForTag(pyxb.namespace.ExpandedName(None, 'irq')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 139, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(resourcesType._UseForTag(pyxb.namespace.ExpandedName(None, 'ioPort')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 140, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
resourcesType._Automaton = _BuildAutomaton_2()




memRegionsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'memory'), memoryType, scope=memRegionsType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 213, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(memRegionsType._UseForTag(pyxb.namespace.ExpandedName(None, 'memory')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 213, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
memRegionsType._Automaton = _BuildAutomaton_3()




memoryRefsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'memory'), memRefType, scope=memoryRefsType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 218, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(memoryRefsType._UseForTag(pyxb.namespace.ExpandedName(None, 'memory')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 218, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
memoryRefsType._Automaton = _BuildAutomaton_4()




physicalMemoryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'memoryBlock'), memoryBlockType, scope=physicalMemoryType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 276, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 276, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(physicalMemoryType._UseForTag(pyxb.namespace.ExpandedName(None, 'memoryBlock')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 276, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
physicalMemoryType._Automaton = _BuildAutomaton_5()




platformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'processor'), processorType, scope=platformType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 281, 3)))

platformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'memory'), physicalMemoryType, scope=platformType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 282, 3)))

platformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'devices'), devicesType, scope=platformType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 283, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(platformType._UseForTag(pyxb.namespace.ExpandedName(None, 'processor')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 281, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(platformType._UseForTag(pyxb.namespace.ExpandedName(None, 'memory')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 282, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(platformType._UseForTag(pyxb.namespace.ExpandedName(None, 'devices')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 283, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
platformType._Automaton = _BuildAutomaton_6()




deviceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'pci'), pciType, scope=deviceType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 42, 3)))

deviceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'irq'), irqType, scope=deviceType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 43, 3)))

deviceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'memory'), deviceMemoryType, scope=deviceType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 44, 3)))

deviceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ioPort'), ioPortType, scope=deviceType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 45, 3)))

deviceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'capabilities'), capabilitiesType, scope=deviceType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 46, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 42, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 43, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 44, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 45, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 46, 3))
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(deviceType._UseForTag(pyxb.namespace.ExpandedName(None, 'pci')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 42, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(deviceType._UseForTag(pyxb.namespace.ExpandedName(None, 'irq')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 43, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(deviceType._UseForTag(pyxb.namespace.ExpandedName(None, 'memory')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 44, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(deviceType._UseForTag(pyxb.namespace.ExpandedName(None, 'ioPort')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 45, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(deviceType._UseForTag(pyxb.namespace.ExpandedName(None, 'capabilities')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 46, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
deviceType._Automaton = _BuildAutomaton_7()




devicesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'device'), deviceType, scope=devicesType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 68, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 68, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(devicesType._UseForTag(pyxb.namespace.ExpandedName(None, 'device')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 68, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
devicesType._Automaton = _BuildAutomaton_8()




deviceRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'pci'), pciType, scope=deviceRefType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 120, 3)))

deviceRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'memory'), memRefType, scope=deviceRefType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 121, 3)))

deviceRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ioPort'), ioPortRefType, scope=deviceRefType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 122, 3)))

deviceRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'irq'), irqRefType, scope=deviceRefType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 123, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 120, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 121, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 122, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 123, 3))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(deviceRefType._UseForTag(pyxb.namespace.ExpandedName(None, 'pci')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 120, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(deviceRefType._UseForTag(pyxb.namespace.ExpandedName(None, 'memory')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 121, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(deviceRefType._UseForTag(pyxb.namespace.ExpandedName(None, 'ioPort')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 122, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(deviceRefType._UseForTag(pyxb.namespace.ExpandedName(None, 'irq')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 123, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
deviceRefType._Automaton = _BuildAutomaton_9()




memoryBaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'file'), fileContentType, scope=memoryBaseType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 229, 3)))

memoryBaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'fill'), fillContentType, scope=memoryBaseType, location=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 230, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 228, 2))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(memoryBaseType._UseForTag(pyxb.namespace.ExpandedName(None, 'file')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 229, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(memoryBaseType._UseForTag(pyxb.namespace.ExpandedName(None, 'fill')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 230, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
memoryBaseType._Automaton = _BuildAutomaton_10()




def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 228, 2))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(memoryType._UseForTag(pyxb.namespace.ExpandedName(None, 'file')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 229, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(memoryType._UseForTag(pyxb.namespace.ExpandedName(None, 'fill')), pyxb.utils.utility.Location('/home/cj/Programming/muen/tools/libmuxml/generated/platform_config.xsd', 230, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
memoryType._Automaton = _BuildAutomaton_11()

