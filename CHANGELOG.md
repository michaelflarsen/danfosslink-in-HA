# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Support for setpoint control (currently read-only)
- Docker compose setup for easier deployment
- Automated flow export/import tools
- Multi-language support (English, German, Swedish)
- Web UI for configuration

---

## [1.2.0] - 2026-03-07

### Added
- 📚 Comprehensive documentation structure
  - Installation guide (`docs/INSTALLATION.md`)
  - Alexa setup guide (`docs/SETUP_ALEXA.md`)
  - Configuration guide (`docs/CONFIGURATION.md`)
  - Troubleshooting guide (`docs/TROUBLESHOOTING.md`)
- 📁 Project restructuring
  - `flows/` directory for Node-RED flows
  - `docs/` directory for documentation
  - `assets/` directory for images
  - `config/` directory for configuration examples
- 🎨 Improved README with table of contents
- ✅ Professional project structure
- 📝 CHANGELOG.md for version tracking

### Improved
- Better organized documentation
- Cleaner project layout
- More user-friendly setup process
- Enhanced error handling guidance

### Documentation
- Updated all links to new structure
- Added troubleshooting section
- Added configuration examples
- Added quick-start guide

---

## [1.1.0] - 2026-02-15

### Added
- Support for 8 rooms by default
- Home Assistant sensor integration
- Temperature and setpoint monitoring
- 5-minute update frequency via Alexa
- Node-RED flow export option

### Fixed
- Improved data indexing function
- Better error messages in Node-RED

### Known Issues
- Setpoint control not yet supported (read-only)
- Limited to 8 rooms without manual expansion
- 5-minute polling limitation from Alexa API

---

## [1.0.0] - 2026-01-01

### Initial Release
- Initial Node-RED flow for Danfoss integration
- Basic temperature monitoring
- Alexa API integration
- Home Assistant connectivity
- Support for up to 8 rooms

### Features
- Temperature reading from Danfoss Link CC via Alexa
- Data processing in Node-RED
- Integration with Home Assistant
- Debug capabilities
- Basic documentation

### Known Limitations
- Only 8 rooms supported
- Read-only temperature values
- 5-minute update limitation
- Limited error handling

---

## Version History

| Version | Date | Type | Status |
|---------|------|------|--------|
| 1.2.0 | 2026-03-07 | Release | ✅ Stable |
| 1.1.0 | 2026-02-15 | Release | ✅ Stable |
| 1.0.0 | 2026-01-01 | Initial | ⚠️ Legacy |

---

## Upgrade Guide

### From 1.1.0 to 1.2.0

⚠️ **No breaking changes** - fully backward compatible

**What to do:**
1. Update documentation from new `docs/` folder
2. Review new troubleshooting guide
3. No changes needed to Node-RED flow
4. No changes needed to HA configuration

**Step by step:**
```bash
# Pull latest changes
git pull origin main

# Review new docs
cd docs/
ls -la

# No flow update needed - existing setup still works!
```

### From 1.0.0 to 1.1.0

**Breaking changes:** None

**New files:**
- Updated Node-Red flow with better structure
- Additional sensor configurations

---

## Dependencies

- **Node-RED** ≥ 2.0.0
- **node-red-contrib-home-assistant-websocket** - Latest
- **node-red-contrib-alexa-remote2-applestrudel** - Latest
- **Home Assistant** ≥ 2023.1.0
- **Danfoss Link CC** - Latest firmware

---

## Security

### Version 1.2.0
- ✅ No known security issues
- Uses official Home Assistant API
- Uses official Amazon Alexa API
- Credentials stored securely in Node-RED

### Reporting Security Issues

⚠️ Please do NOT open public issues for security problems

Instead, email: [maintainer-email]

---

## Future Roadmap

### Planned for v1.3.0 (Q2 2026)
- [ ] Setpoint control implementation
- [ ] Multi-user authentication
- [ ] Advanced filtering & averaging
- [ ] Custom alert rules

### Planned for v2.0.0 (Q4 2026)
- [ ] Web UI for configuration
- [ ] Mobile app integration
- [ ] GraphQL API
- [ ] Direct Danfoss API (if available)

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## Thanks To

- Michael F. Larsen (Original creator & maintainer)
- Community contributors
- Node-RED team
- Home Assistant team
- Danfoss & Amazon for their APIs

---

**Last updated:** March 2026  
**Maintainer:** Michael F. Larsen  
**Project:** Danfoss Link CC → Home Assistant Integration
