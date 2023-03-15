# How to pass the payload for a device?

Answer: To pass the payload for a device, you can use the attributes of the POJO class provided, such as "enabled", "extensions", "defaults", "via", "viaGroups", "memberOf", "status", "downstreamMessageMapper", "upstreamMessageMapper", "authorities", and "commandEndpoint".

# If possible, how to change/update the feature in Hono?

Answer: Currently, there is no attribute called "feature" in Hono. 

# Why it is not possible to change/update the feature in Hono?

Answer: It is not possible to change/update the feature in Hono because there is no attribute called "feature" in Hono. If there is a need to add this attribute, we need to modify source code.
 

 
 
 # pojo class
  @JsonProperty(RegistryManagementConstants.FIELD_ENABLED)
    private Boolean enabled;

    @JsonProperty(RegistryManagementConstants.FIELD_EXT)
    @JsonInclude(value = Include.NON_EMPTY)
    private Map<String, Object> extensions = new HashMap<>();

    @JsonProperty(RegistryManagementConstants.FIELD_PAYLOAD_DEFAULTS)
    @JsonInclude(value = Include.NON_EMPTY)
    private Map<String, Object> defaults = new HashMap<>();

    @JsonProperty(RegistryManagementConstants.FIELD_VIA)
    @JsonInclude(value = Include.NON_EMPTY)
    @JsonFormat(with = JsonFormat.Feature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
    private List<String> via = new ArrayList<>();

    @JsonProperty(RegistryManagementConstants.FIELD_VIA_GROUPS)
    @JsonInclude(value = Include.NON_EMPTY)
    @JsonFormat(with = JsonFormat.Feature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
    private List<String> viaGroups = new ArrayList<>();

    @JsonProperty(RegistryManagementConstants.FIELD_MEMBER_OF)
    @JsonInclude(value = Include.NON_EMPTY)
    @JsonFormat(with = JsonFormat.Feature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
    private List<String> memberOf = new ArrayList<>();

    @JsonProperty(RegistryManagementConstants.FIELD_STATUS)
    @JsonInclude(value = Include.NON_EMPTY)
    private DeviceStatus status;

    @JsonProperty(RegistryManagementConstants.FIELD_DOWNSTREAM_MESSAGE_MAPPER)
    private String downstreamMessageMapper;

    @JsonProperty(RegistryManagementConstants.FIELD_UPSTREAM_MESSAGE_MAPPER)
    private String upstreamMessageMapper;

    @JsonProperty(RegistryManagementConstants.FIELD_AUTHORITIES)
    @JsonInclude(value = Include.NON_EMPTY)
    private Set<String> authorities = new HashSet<>();

    @JsonProperty(RegistryManagementConstants.COMMAND_ENDPOINT)
    private CommandEndpoint commandEndpoint;
